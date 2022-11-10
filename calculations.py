# Prototype of time series spreadsheet for retirement calculator

# Imports
import numpy as np
import pandas as pd
import numpy as np
import numpy_financial as npf

from Income_Tax import (Income_tax_calc, Net_to_gross_tax_calc)

#initial values
start_year=2021
state_pension_age=66
state_pension_income=9000
PCLS_factor=0.25
minimum_pension_age=57

#Variables that are used in multiple calculations below - as dictionary (so they can prepopulate assumptions page)


#Assumptions behind calculator - can be edited in setttings

class Assumptions:
    def __init__(self, ER_Max_LTV_c, yearly_planned_returns_c, hpi_growth_c, mortgage_interest_rate_c, equity_release_rate_c, cash_savings_returns_c, buffer_multiple_c, drawdown_adjustment_factor_c, buffer_lead_time_c) :
        self.ER_Max_LTV_c=ER_Max_LTV_c
        self.yearly_planned_returns_c=yearly_planned_returns_c
        self.hpi_growth_c=hpi_growth_c
        self.mortgage_interest_rate_c=mortgage_interest_rate_c
        self.equity_release_rate_c=equity_release_rate_c
        self.cash_savings_returns_c=cash_savings_returns_c
        self.buffer_multiple_c=buffer_multiple_c  #Number of X yearly planned withdrawals we want to keep as cash
        self.drawdown_adjustment_factor_c=drawdown_adjustment_factor_c  #speed with which we adjust down/up drawdown based on cumulative investment performance
        self.buffer_lead_time_c=buffer_lead_time_c #number of years before retirement where we start selling down assets to build up cash buffer towards target


assumptions_used=Assumptions(ER_Max_LTV_c=0.2, yearly_planned_returns_c=0.02, hpi_growth_c=0.01,mortgage_interest_rate_c=0.02, equity_release_rate_c=0.04, cash_savings_returns_c=0.001, buffer_multiple_c=5.00, drawdown_adjustment_factor_c=10, buffer_lead_time_c=3.00  )


#Inputs that cusotmer enters first time in

class Inputs:
    def __init__(self, age_now_c, target_retirement_age_c, target_income_pa_c, pension_value_now_c, planned_pension_contributions_pa_c, db_pension_income_c, db_pension_start_age_c, ISA_value_now_c, planned_ISA_contributions_pa_c, house_value_now_c, mortgage_value_now_c, years_left_on_mortgage_c, cash_savings_now_c, planned_cash_savings_contributions_pa_c):
        self.age_now=age_now_c
        self.target_retirement_age=target_retirement_age_c
        self.target_income_pa=target_income_pa_c
        self.pension_value_now=pension_value_now_c
        self.planned_pension_contributions_pa=planned_pension_contributions_pa_c
        self.db_pension_income=db_pension_income_c
        self.db_pension_start_age=db_pension_start_age_c
        self.ISA_value_now=ISA_value_now_c
        self.planned_ISA_contributions_pa=planned_ISA_contributions_pa_c
        self.house_value_now=house_value_now_c
        self.mortgage_value_now=mortgage_value_now_c
        self.years_left_on_mortgage=years_left_on_mortgage_c
        self.cash_savings_now=cash_savings_now_c
        self.planned_cash_savings_contributions_pa=planned_cash_savings_contributions_pa_c


inputs_used=Inputs(age_now_c=None, target_retirement_age_c=None, target_income_pa_c=None, pension_value_now_c=None, planned_pension_contributions_pa_c=None, db_pension_income_c=None, db_pension_start_age_c=None, ISA_value_now_c=None, planned_ISA_contributions_pa_c=None, house_value_now_c=None, mortgage_value_now_c=None, years_left_on_mortgage_c=None, cash_savings_now_c=None, planned_cash_savings_contributions_pa_c=None)









#Value of Pension Investments over time
def Pension_Investment_forecast(age_now, retirement_age,target_income_pa, pension_value_now=0, planned_pension_contributions_pa=0, db_pension_income=0, db_pension_start_age=0, ISA_value_now=0, planned_ISA_contributions_pa=0, house_value_now=0, mortgage_value_now=0, years_left_on_mortgage=1, cash_savings_now=0, planned_cash_saving_contributions_pa=0):
    ER_max_LTV = assumptions_used.ER_Max_LTV_c
    yearly_planned_returns = assumptions_used.yearly_planned_returns_c
    hpi_growth = assumptions_used.hpi_growth_c
    mortgage_interest_rate = assumptions_used.mortgage_interest_rate_c
    equity_release_rate = assumptions_used.equity_release_rate_c
    cash_savings_returns=assumptions_used.cash_savings_returns_c
    buffer_multiple=assumptions_used.buffer_multiple_c
    drawdown_adjustment_factor=assumptions_used.drawdown_adjustment_factor_c
    buffer_lead_time =assumptions_used.buffer_lead_time_c



    #Initial Calculations
    horizon_time = 120 - int(age_now)
    horizon_date = start_year + horizon_time
    pension_start_year = retirement_age - age_now + start_year
    db_pension_start_year=db_pension_start_age-age_now+start_year
    state_pension_start_year=start_year+66-age_now
    target_buffer=buffer_multiple*target_income_pa #size of cash buffer we want the savings account to equal during drawdown
    buffer_start_year = pension_start_year - buffer_lead_time  #when to start building buffer
    year_can_access_pension=start_year+minimum_pension_age-age_now

    # Create year as list item
    year = [start_year + i for i in range(0, horizon_time)]

    # Create year as dataframe series
    year_calc = pd.Series(index=year)
    year_calc[start_year] = start_year
    for i in range(start_year + 1, horizon_date):
        year_calc[i] = year_calc[i - 1] + 1

    # Initialisation of variables used in loop below
    age = pd.Series(index=year)

    pension_start = pd.Series(index=year)
    pension_end = pd.Series(index=year)
    pension_investment_return = pd.Series(index=year)
    pension_contribution=pd.Series(index=year)
    pension_withdrawal = pd.Series(index=year)
    pension_lump_sum = pd.Series(index=year)

    #Investment ISA
    ISA_start = pd.Series(index=year)
    ISA_end = pd.Series(index=year)
    ISA_investment_return = pd.Series(index=year)
    ISA_contribution = pd.Series(index=year)
    ISA_withdrawal = pd.Series(index=year)

    #Cash savings buffer
    cash_savings_start=pd.Series(index=year)
    cash_savings_return=pd.Series(index=year)
    cash_savings_contribution=pd.Series(index=year)#additional savings before retirement (not drawdown top ups)
    cash_savings_withdrawal=pd.Series(index=year)
    cash_savings_drawdown_top_up=pd.Series(index=year)#top ups after selling down units from pension or isa
    cash_savings_end=pd.Series(index=year)

    state_pension=pd.Series(index=year)
    db_pension=pd.Series(index=year)

    tax_paid=pd.Series(index=year)
    property_equity_start=pd.Series(index=year)

    net_income=pd.Series(index=year)

    income_gap = pd.Series(index=year)


    house_value_start = pd.Series(index=year)
    house_value_end = pd.Series(index=year)
    house_value_increase=pd.Series(index=year)


    mortgage_value_start = pd.Series(index=year)
    mortgage_value_end = pd.Series(index=year)
    mortgage_value_increase = pd.Series(index=year)

    equity_release_mortgage_start = pd.Series(index=year)
    equity_release_mortgage_end = pd.Series(index=year)
    equity_released = pd.Series(index=year)
    equity_release_interest_charge=pd.Series(index=year)


    yearly_returns=pd.Series(index=year)
    yearly_returns_index=pd.Series(index=year)
    cumulative_returns_index=pd.Series(index=year)
    cumulative_planned_returns_index=pd.Series(index=year)
    ratio_cumulative_returns_vs_plan=pd.Series(index=year)
    drawdown_adjustment=pd.Series(index=year)



    target_income_inc_mtg = pd.Series(index=year)
    target_income_after_state_db_pension=pd.Series(index=year)
    target_drawdown=pd.Series(index=year)


    mortgage_payment=npf.pmt(float(mortgage_interest_rate)/12,years_left_on_mortgage*12,mortgage_value_now)*12


    # Loop to calculate cashflow each year
    for i in range(start_year, horizon_date):
        In_retirement = i >= pension_start_year


        #Calculation of investment returns and associated indices
        yearly_returns[i]=yearly_planned_returns #change to randomised variable for monte carlo simulation
        yearly_returns_index[i]=1+yearly_returns[i]
        cumulative_returns_index[start_year]=1 #year (i+1) and onwards defined at end of loop
        cumulative_planned_returns_index[start_year]=1 #year (i+1) and onwards defined at end of loop
        ratio_cumulative_returns_vs_plan[i]=cumulative_returns_index[i]/cumulative_planned_returns_index[i] #ratio to drive drawdown_adjustment
        drawdown_adjustment[i]=ratio_cumulative_returns_vs_plan[i]**drawdown_adjustment_factor #factor used to reflect whether cumulative investment performance is above trend or below - to be multiplied against planned withdrawal to refresh savings account



        #Initial values
        pension_start[start_year] = pension_value_now
        ISA_start[start_year]=ISA_value_now
        house_value_start[start_year]=house_value_now
        mortgage_value_start[start_year]=np.where(mortgage_value_now>0,-1*mortgage_value_now,0)
        equity_release_mortgage_start[start_year]=0
        cash_savings_start[start_year]=cash_savings_now


        #Age
        age[i] = age_now + i - start_year


        #Returns for different types of asset
        pension_investment_return[i] = pension_start[i] * float(yearly_returns[i])
        ISA_investment_return[i]=ISA_start[i]*float(yearly_returns[i])
        house_value_increase[i]=house_value_start[i]*float(hpi_growth)
        mortgage_value_increase[i]=mortgage_value_now/years_left_on_mortgage if mortgage_value_start[i]<0 else 0
        equity_release_interest_charge[i] =equity_release_mortgage_start[i]*float(equity_release_rate)
        cash_savings_return[i]=cash_savings_start[i]*float(cash_savings_returns)

        #Pension lump sum
        pension_lump_sum[i] = np.where(i==year_can_access_pension, pension_start[i] * PCLS_factor,0)

        #contributions before retirement
        pension_contribution[i] = np.where(i < pension_start_year, planned_pension_contributions_pa,0)
        ISA_contribution[i]=np.where(i<pension_start_year,planned_ISA_contributions_pa,0)
        cash_savings_contribution[i]= np.where(i < pension_start_year, planned_cash_saving_contributions_pa,0)

        #Target income after factoring in cost of mortgage
        target_income_inc_mtg[i] = np.where(i>=pension_start_year, np.where(mortgage_value_start[i] < 0, target_income_pa - mortgage_payment, target_income_pa),0)


        #money needed from savings/investing after taking into account state and db pensions
        state_pension[i] = np.where(i >= state_pension_start_year, state_pension_income, 0)
        db_pension[i] = np.where(i >= db_pension_start_year, float(db_pension_income), 0)
        target_income_after_state_db_pension[i]=target_income_inc_mtg[i]-Income_tax_calc(state_pension[i] + db_pension[i])[1]

        #This is met by withdrawing from savings buffer
        cash_savings_withdrawal[i]=min(cash_savings_start[i],target_income_after_state_db_pension[i])

        #now need to refresh by drawing down

        target_drawdown[i]=np.where(i<buffer_start_year,0,np.where(((i>=buffer_start_year) & (i<pension_start_year)==True),max(target_buffer-cash_savings_start[i]-cash_savings_return[i]-cash_savings_contribution[i],0)/(pension_start_year-year_calc[i]),  np.where(cash_savings_start[i]<target_buffer*1.1, target_income_after_state_db_pension[i]*drawdown_adjustment[i],0))) #drawdown of ISAs and pensions needed to sustain income.


        #Assign meeting this target_drawdown to ISAs then Pension pot.
        ISA_withdrawal[i]= min(ISA_start[i],target_drawdown[i])
        pension_withdrawal[i] = np.where(i>=year_can_access_pension, min(pension_start[i]-pension_lump_sum[i], Net_to_gross_tax_calc(target_drawdown[i]-ISA_withdrawal[i])),0)  #Can only access pension at age 57
        equity_released[i]=min(max(house_value_start[i]*float(ER_max_LTV)+equity_release_mortgage_start[i],0),(target_drawdown[i]-ISA_withdrawal[i]-Income_tax_calc(pension_withdrawal[i])[1]))
        cash_savings_drawdown_top_up[i]=ISA_withdrawal[i]+Income_tax_calc(pension_withdrawal[i])[1]+equity_released[i]

        #End of year positions for each asset
        cash_savings_end[i]=cash_savings_start[i]+cash_savings_return[i]+cash_savings_contribution[i]-cash_savings_withdrawal[i]+cash_savings_drawdown_top_up[i]
        pension_end[i] = pension_start[i] + pension_investment_return[i] - pension_lump_sum[i]+pension_contribution[i] - pension_withdrawal[i]
        ISA_end[i]=ISA_start[i] + ISA_investment_return[i] + pension_lump_sum[i]+ISA_contribution[i] - ISA_withdrawal[i]
        house_value_end[i] = house_value_start[i]+house_value_increase[i]
        mortgage_value_end[i] = mortgage_value_start[i]+mortgage_value_increase[i]
        equity_release_mortgage_end[i] = max(equity_release_mortgage_start[i]+equity_release_interest_charge[i]-equity_released[i],house_value_end[i]*-1)

        #value for next period - where needed
        cash_savings_start[i+1]=cash_savings_end[i]
        pension_start[i + 1] = pension_end[i]
        ISA_start[i+1] = ISA_end[i]
        house_value_start[i+1]=house_value_end[i]
        mortgage_value_start[i+1]=mortgage_value_end[i]
        equity_release_mortgage_start[i+1]=equity_release_mortgage_end[i]
        cumulative_returns_index[i+1] = cumulative_returns_index[i] * yearly_returns_index[i]
        cumulative_planned_returns_index[i+1]=(1+yearly_planned_returns)**(i-start_year+1)

        tax_paid[i]=Income_tax_calc(pension_withdrawal[i]+state_pension[i]+db_pension[i])[0]
        property_equity_start[i]=house_value_start[i]+mortgage_value_start[i]+equity_release_mortgage_start[i]

        net_income[i]=cash_savings_withdrawal[i]+Income_tax_calc(state_pension[i]+db_pension[i])[1]


        income_gap[i]=np.where(i >= pension_start_year,net_income[i]-target_income_inc_mtg[i],0)


    # Output
    calc_output_all = pd.DataFrame([round(year_calc),round(age), round(target_income_inc_mtg), round(target_income_after_state_db_pension), round(cumulative_returns_index,3)*100, round(cumulative_planned_returns_index,3)*100, round(drawdown_adjustment,3)*100,  round(cash_savings_start), round(cash_savings_return), round(cash_savings_contribution), round(cash_savings_withdrawal), round(target_drawdown), round(cash_savings_drawdown_top_up), round(pension_start), round(pension_investment_return), round(pension_contribution),round(pension_withdrawal), round(pension_end), round(ISA_start), round(ISA_investment_return), round(ISA_contribution),round(ISA_withdrawal), round(ISA_end), round(state_pension),round(db_pension),round(tax_paid), round(house_value_start), round(mortgage_value_start), round(equity_release_mortgage_start),round(property_equity_start), round(equity_released),round(net_income), round(income_gap)],
                          index=['Year','Age',  'Target_Income_Inc_Mtg', 'Target_Income_After_State_DB_Pension','Cumulative_Returns_Index', 'Cumulative_Planned_Returns_Index','Drawdown_Adjustment', 'Cash_Savings_Start','Cash_Savings_Return','Cash_Savings_Contribution',  'Cash_Savings_Withdrawal', 'Target_Drawdown', 'Cash_Savings_Drawdown_Top_Up', 'Pension_Portfolio_Start', 'Pension_Investment_Return', 'Pension_Contribution', 'Pension_Withdrawal', 'Pension_Portfolio_End', 'ISA_Start', 'ISA_Return', 'ISA_Contribution', 'ISA_Withdrawal', 'ISA_End','State_Pension', 'DB_Pension','Tax_Paid', 'House_Value_Start', 'Mortgage_Value_Start', 'Equity_Release_Mortgage_start', 'Property_Equity_Start', 'Equity_Released', 'Net_Income', 'Income_Gap'])
    #Drop last column to avoid NaN result
    calc_output=calc_output_all.iloc[:,:-1]

    #Calculate age where income first insufficient
    income_gap = (pd.DataFrame(calc_output_all.loc['Income_Gap']))
    Has_min = income_gap['Income_Gap'].min() < 0

    if Has_min == True:
        date_of_first_income_gap = (income_gap[income_gap['Income_Gap'] < 0].index[0])
        age_of_first_income_gap = int(date_of_first_income_gap) - start_year + age_now

    else:
        age_of_first_income_gap = "No gap in income"

    #create table
    output_transposed = calc_output.loc[['Age', 'Target_Income_Inc_Mtg', 'Target_Income_After_State_DB_Pension','Cumulative_Returns_Index', 'Cumulative_Planned_Returns_Index','Drawdown_Adjustment','Cash_Savings_Start','Cash_Savings_Return','Cash_Savings_Contribution',  'Cash_Savings_Withdrawal', 'Target_Drawdown','Cash_Savings_Drawdown_Top_Up','Pension_Portfolio_Start','Pension_Investment_Return', 'Pension_Contribution', 'Pension_Withdrawal', 'Pension_Portfolio_End', 'ISA_Start', 'ISA_Return', 'ISA_Contribution', 'ISA_Withdrawal', 'ISA_End','State_Pension','DB_Pension', 'Tax_Paid', 'House_Value_Start', 'Mortgage_Value_Start', 'Equity_Release_Mortgage_start', 'Property_Equity_Start','Equity_Released', 'Net_Income',]].transpose()
    format_dict = {'Age': '{0:.0f}',  'Target_Income_Inc_Mtg':'{0:.0f}', 'Target_Income_After_State_DB_Pension':'{0:.0f}', 'Cumulative_Returns_Index':'{0:.0f}', 'Cumulative_Planned_Returns_Index':'{0:.0f}','Drawdown_Adjustment':'{0:.0f}','Cash_Savings_Start': '{0:.0f}','Cash_Savings_Return': '{0:.0f}','Cash_Savings_Contribution': '{0:.0f}',  'Cash_Savings_Withdrawal': '{0:.0f}', 'Target_Drawdown': '{0:.0f}', 'Cash_Savings_Drawdown_Top_Up': '{0:.0f}','Pension_Portfolio_Start': '£{0:,.0f}', 'Pension_Investment_Return': '£{0:,.0f}','Pension_Contribution':'£{0:,.0f}',
                   'Pension_Withdrawal': '£{0:,.0f}', 'Pension_Portfolio_End': '£{0:,.0f}','ISA_Start': '£{0:,.0f}', 'ISA_Return': '£{0:,.0f}', 'ISA_Contribution': '£{0:,.0f}', 'ISA_Withdrawal': '£{0:,.0f}', 'ISA_End': '£{0:,.0f}','State_Pension': '£{0:,.0f}','DB_Pension': '£{0:,.0f}', 'Tax_Paid': '£{0:,.0f}',  'House_Value_Start': '£{0:,.0f}', 'Mortgage_Value_Start': '£{0:,.0f}', 'Equity_Release_Mortgage_start': '£{0:,.0f}','Property_Equity_Start':'£{0:,.0f}', 'Equity_Released': '£{0:,.0f}', 'Net_Income': '£{0:,.0f}'}
    output_transposed_formatted = output_transposed.style.format(format_dict)
    Table = output_transposed_formatted.to_html(table_uuid="table_df")

    # Values for Summary table
    Pension_Values=(calc_output.loc[['Pension_Portfolio_Start']])
    ISA_Values = (calc_output.loc[['ISA_Start']])
    Max_Pension_Investment_Value=(Pension_Values.max(axis=1)).get('Pension_Portfolio_Start')
    Max_Pension_Investment_Value_Formatted = "£{:,.0f}".format(Max_Pension_Investment_Value)
    Max_ISA_Value = "£{:,.0f}".format((ISA_Values.max(axis=1)).get('ISA_Start'))



    return{"timeseries":calc_output, "age_gap":age_of_first_income_gap, "detailed_results":Table, "max_pension": Max_Pension_Investment_Value, "max_pension_formatted": Max_Pension_Investment_Value_Formatted,"max_isa":Max_ISA_Value}


