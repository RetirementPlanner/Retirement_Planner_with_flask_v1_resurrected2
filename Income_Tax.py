#Calculation of Income Tax

def Income_tax_calc(gross_taxable_income):
    #Settings
    Personal_allowance_threshold=12570
    Basic_rate_threshold=50270
    Higher_rate_threshold=150000
    Basic_rate_tax_rate = 0.2
    Higher_rate_tax_rate=0.4
    Additional_rate_tax_rate=0.45

    #Gross Income in each income band
    Tax_free_income=min(gross_taxable_income, Personal_allowance_threshold)
    Basic_rate_taxed_income=min(gross_taxable_income-Tax_free_income, Basic_rate_threshold-Personal_allowance_threshold)
    Higher_rate_taxed_income=min(gross_taxable_income-Basic_rate_taxed_income-Tax_free_income, Higher_rate_threshold-Basic_rate_threshold)
    Additional_rate_taxed_income=gross_taxable_income-Higher_rate_taxed_income-Basic_rate_taxed_income-Tax_free_income

    #Tax Calc
    Tax = Basic_rate_taxed_income*Basic_rate_tax_rate\
        +Higher_rate_taxed_income*Higher_rate_tax_rate\
          +Additional_rate_taxed_income*Additional_rate_tax_rate

    Net_Income=gross_taxable_income-Tax

    return(Tax, Net_Income)

def Net_to_gross_tax_calc(net_income_post_tax):
    #Settings
    Personal_allowance_threshold=12570
    Basic_rate_threshold=50270
    Higher_rate_threshold=150000
    Basic_rate_tax_rate = 0.2
    Higher_rate_tax_rate=0.4
    Additional_rate_tax_rate=0.45

    # Gross Income in each income band
    Net_income_no_tax = min(net_income_post_tax, Personal_allowance_threshold)
    Net_income_basic_rate_tax = min(net_income_post_tax - Net_income_no_tax, (Basic_rate_threshold-Personal_allowance_threshold)*(1-Basic_rate_tax_rate))
    Net_income_higher_rate_tax = min(net_income_post_tax - Net_income_basic_rate_tax - Net_income_no_tax, (Higher_rate_threshold-Basic_rate_threshold)*(1-Higher_rate_tax_rate))
    Net_income_additional_rate_tax = net_income_post_tax - Net_income_higher_rate_tax - Net_income_basic_rate_tax - Net_income_no_tax

    #Gross Income calc
    Gross_Income=Net_income_no_tax+\
    Net_income_basic_rate_tax/(1-Basic_rate_tax_rate)+\
    Net_income_higher_rate_tax/(1-Higher_rate_tax_rate)+\
    Net_income_additional_rate_tax/(1-Additional_rate_tax_rate)

    return(Gross_Income)


