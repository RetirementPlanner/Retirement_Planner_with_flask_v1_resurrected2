#Flask View page

from flask import (Flask,render_template,abort, request, redirect, url_for)
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional
import numpy as np
from calculations import *
from insights import *

import pandas as pd



output={}

#set up form data fields.  make sure this matches the object names if you want it to prefill!


class Enter_Details_Form(FlaskForm):
    age_now_c = IntegerField('Age Now *', validators=[InputRequired('Please enter age'),])
    target_retirement_age_c = IntegerField('Target retirement age *', validators=[InputRequired(),])
    pension_value_now_c = IntegerField('Value of pensions pots now (£)', validators=[Optional(),])
    planned_pension_contributions_pa_c = IntegerField('Yearly contributions to pension pots (£pa)', validators=[Optional(),])
    ISA_value_now_c = IntegerField('Value of your other investments now (e.g. ISAs, £)', validators=[Optional(), ])
    planned_ISA_contributions_pa_c = IntegerField('Additional amount invested each year  (£pa)', validators=[Optional(), ])
    db_pension_income_c = IntegerField('Value of any Final Salary pension (£pa)', validators=[Optional()])
    db_pension_start_age_c = IntegerField('Start age of any Final Salary pension', validators=[Optional()])
    house_value_now_c = IntegerField('Value of your home (if you own it) (£)', validators=[Optional(), ])
    mortgage_value_now_c = IntegerField('Value of mortgage on your home (£)', validators=[Optional(), ])
    years_left_on_mortgage_c = IntegerField('Number of years left to repay mortgage', validators=[Optional(), ])
    target_income_pa_c = IntegerField('Income you want in retirement (net £pa) * ', validators=[InputRequired()])
    cash_savings_now_c=IntegerField('Value of cash savings (£)', validators=[Optional()])
    planned_cash_savings_contributions_pa_c=IntegerField('Addition to cash savings each year (£pa)', validators=[Optional()])



class Set_Assumptions_Form(FlaskForm):
    yearly_planned_returns_c=SelectField('Expected real Investment Returns (%pa)', choices=[(0.01,'1%'),(0.02,'2%'), (0.03,'3%'),(0.04,'4%')])
    hpi_growth_c=SelectField('Expected real house price growth (%pa)', choices=[(0.01,'1%'),(0.02,'2%'), (0.03,'3%'),(0.04,'4%')])
    mortgage_interest_rate_c=SelectField('Expected real mortgage interest rates (%pa)', choices=[(0.01,'1%'),(0.02,'2%'), (0.03,'3%'),(0.04,'4%')])
    equity_release_rate_c=SelectField('Expected real equity release interest rate (%pa)', choices=[(0.01,'1%'),(0.02,'2%'), (0.03,'3%'),(0.04,'4%')])
    ER_Max_LTV_c=SelectField('Maximum Loan to Value Ratio of Equity Release (%)', choices=[(0,'0%'),(0.1,'10%'),(0.2,'20%'),(0.3,'30%'), (0.4,'40%'),(0.5,'50%'), (0.6,'60%')])
    buffer_multiple_c=SelectField('Number of years income to keep in cash as buffer', choices=[(1.00,1), (2.00,2),(3.00,3),(4.00,4),(5.00,5) ])
    drawdown_adjustment_factor_c=SelectField('Sensitivity of how quickly cash buffer is replemished', choices=[(1,'Low'), (10, 'Medium'), (30,'High')])
    buffer_lead_time_c=SelectField('How soon before retirement when investments start to be sold to build cash buffer', choices=[(1.00, '1 Year'), (3.00, '3 Years'), (5.00, '5 Years')])


app= Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsASecret!'




@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/calculator_inputs", methods=["GET","POST"])
def calculator_inputs():

    form=Enter_Details_Form(obj=inputs_used)

    if form.validate_on_submit():
      # form has been submitted, process data FORCE THESE VALUES TO FLOATS SO THAT INSIGHTS WORK

        inputs_used.age_now_c = form.age_now_c.data
        inputs_used.target_retirement_age_c= form.target_retirement_age_c.data
        inputs_used.pension_value_now_c= np.where(type(form.pension_value_now_c.data)==type(None),0,form.pension_value_now_c.data)
        inputs_used.planned_pension_contributions_pa_c = np.where(type(form.planned_pension_contributions_pa_c.data)==type(None),0,form.planned_pension_contributions_pa_c.data)
        inputs_used.ISA_value_now_c = np.where(type(form.ISA_value_now_c.data)==type(None),0,form.ISA_value_now_c.data)
        inputs_used.planned_ISA_contributions_pa_c = np.where(type(form.planned_ISA_contributions_pa_c.data)==type(None),0,form.planned_ISA_contributions_pa_c.data)
        inputs_used.target_income_pa_c= form.target_income_pa_c.data
        inputs_used.db_pension_income_c=np.where(type(form.db_pension_income_c.data)==type(None),0,form.db_pension_income_c.data)
        inputs_used.db_pension_start_age_c=np.where(type(form.db_pension_start_age_c.data)==type(None),0,form.db_pension_start_age_c.data)
        inputs_used.house_value_now_c= np.where(type(form.house_value_now_c.data) == type(None), 0,form.house_value_now_c.data)
        inputs_used.mortgage_value_now_c= np.where(type(form.mortgage_value_now_c.data) == type(None), 0,form.mortgage_value_now_c.data)
        inputs_used.years_left_on_mortgage_c = np.where(type(form.years_left_on_mortgage_c.data) == type(None), 0,form.years_left_on_mortgage_c.data)
        inputs_used.cash_savings_now_c= np.where(type(form.cash_savings_now_c.data) == type(None), 0, form.cash_savings_now_c.data)
        inputs_used.planned_cash_savings_contributions_pa_c = np.where(type(form.planned_cash_savings_contributions_pa_c.data) == type(None), 0, form.planned_cash_savings_contributions_pa_c.data)

        return redirect(url_for('results_summary'))
    else:
        return render_template("calculator_inputs.html", form=form)

@app.route("/results_summary")
def results_summary():

    #Values for table
    global output
    output=Pension_Investment_forecast(inputs_used.age_now_c, inputs_used.target_retirement_age_c, inputs_used.target_income_pa_c,  inputs_used.pension_value_now_c, inputs_used.planned_pension_contributions_pa_c,  inputs_used.db_pension_income_c, inputs_used.db_pension_start_age_c, inputs_used.ISA_value_now_c, inputs_used.planned_ISA_contributions_pa_c, inputs_used.house_value_now_c, inputs_used.mortgage_value_now_c, inputs_used.years_left_on_mortgage_c, inputs_used.cash_savings_now_c, inputs_used.planned_cash_savings_contributions_pa_c)
    Table = output["detailed_results"]

    #values for summary box
    age_of_first_income_gap_output=output["age_gap"]
    Max_Pension_Investment_Value=output["max_pension_formatted"]
    Max_ISA_Value=output["max_isa"]


    #Values for Pension Valuation chart
    legend_1_PVC = 'Value of Pension Investments(£)'
    legend_2_PVC='Value of Other Investments(£)'
    legend_3_PVC = 'Equity in Property(£)'
    legend_4_PVC = 'Savings/Cash Buffer (£)'
    labels_PVC = [round (num) for num in output["timeseries"].loc["Year"].values.tolist()]
    values_1_PVC = output["timeseries"].loc['Pension_Portfolio_Start'].values.tolist()
    values_2_PVC = output["timeseries"].loc['ISA_Start'].values.tolist()
    values_3_PVC = output["timeseries"].loc['Property_Equity_Start'].values.tolist()
    values_4_PVC= output["timeseries"].loc['Cash_Savings_Start'].values.tolist()

    # Values for Gross Income  chart
    legend_1_Inc = 'State Pension'
    legend_2_Inc = 'DB Pension'
    legend_3_Inc = 'Pension drawdown'
    legend_4_Inc = 'Equity released'
    legend_5_Inc = 'Other Investment drawdown'
    labels_Inc = [round(num) for num in output["timeseries"].loc["Year"].values.tolist()]
    values_1_Inc = output["timeseries"].loc["State_Pension"].values.tolist()
    values_2_Inc = output["timeseries"].loc["DB_Pension"].values.tolist()
    values_3_Inc = output["timeseries"].loc["Pension_Withdrawal"].values.tolist()
    values_4_Inc = output["timeseries"].loc["Equity_Released"].values.tolist()
    values_5_Inc = output["timeseries"].loc["ISA_Withdrawal"].values.tolist()

    # Values for Net Income Chart
    legend_1_Net_Inc = 'Net Income'
    labels_Net_Inc = [round(num) for num in output["timeseries"].loc["Year"].values.tolist()]
    values_1_Net_Inc = output["timeseries"].loc["Net_Income"].values.tolist()


    # Values for Tax paid chart
    legend_Tax = 'Tax Paid (£)'
    labels_Tax = [round(num) for num in output["timeseries"].loc["Year"].values.tolist()]
    values_Tax = output["timeseries"].loc["Tax_Paid"].values.tolist()

    return render_template("results_summary.html",  Max_Pension_Investment_Value=Max_Pension_Investment_Value, Max_ISA_Value=Max_ISA_Value, legend_1_PVC=legend_1_PVC, legend_2_PVC=legend_2_PVC, legend_3_PVC=legend_3_PVC, legend_4_PVC=legend_4_PVC, values_1_PVC=values_1_PVC, values_2_PVC=values_2_PVC, values_3_PVC=values_3_PVC, values_4_PVC=values_4_PVC, labels_PVC=labels_PVC, labels_Inc=labels_Inc, legend_1_Inc=legend_1_Inc, legend_2_Inc=legend_2_Inc, legend_3_Inc=legend_3_Inc, legend_4_Inc=legend_4_Inc, legend_5_Inc=legend_5_Inc, values_1_Inc=values_1_Inc, values_2_Inc=values_2_Inc, values_3_Inc=values_3_Inc, values_4_Inc=values_4_Inc, values_5_Inc=values_5_Inc, legend_Tax=legend_Tax, labels_Tax=labels_Tax, values_Tax=values_Tax, legend_1_Net_Inc=legend_1_Net_Inc, labels_Net_Inc=labels_Net_Inc, values_1_Net_Inc=values_1_Net_Inc, age_of_first_income_gap_output=age_of_first_income_gap_output)

@app.route("/results_data")
def results_data():
    return render_template("results_data.html", table=Table )



#Assumptions form
@app.route("/assumptions_form", methods=["GET","POST"])

def assumptions_form():

    form=Set_Assumptions_Form(obj=assumptions_used)

    if form.validate_on_submit():
      # form has been submitted, process data

        assumptions_used.yearly_planned_returns_c = float(form.yearly_planned_returns_c.data)
        assumptions_used.hpi_growth_c = float(form.hpi_growth_c.data)
        assumptions_used.mortgage_interest_rate_c = float(form.mortgage_interest_rate_c.data)
        assumptions_used.equity_release_rate_c= float(form.equity_release_rate_c.data)
        assumptions_used.ER_Max_LTV_c = float(form.ER_Max_LTV_c.data)
        assumptions_used.buffer_multiple_c = float(form.buffer_multiple_c.data)
        assumptions_used.drawdown_adjustment_factor_c = float(form.drawdown_adjustment_factor_c.data)
        assumptions_used.buffer_lead_time_c = float(form.buffer_lead_time_c.data)

        return redirect(url_for('results_summary'))
    else:
        return render_template("assumptions_form.html", form=form)


#Insights page
@app.route("/insights")
def insights_page():
    Insights_object=Insights(max_pension_value_input=output["max_pension"], planned_ISA_contributions_pa_input=inputs_used.planned_ISA_contributions_pa, planned_cash_savings_contributions_pa_input=inputs_used.planned_cash_savings_contributions_pa)
    Insights_list= Insights_object.extract_insight_list()
    return render_template("insights.html", Insights_list=Insights_list)

#Start app
if __name__ == '__main__':
            app.run()
