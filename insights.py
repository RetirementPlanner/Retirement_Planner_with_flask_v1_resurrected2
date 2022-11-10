


class Insights:
    def __init__(self, max_pension_value_input, planned_ISA_contributions_pa_input, planned_cash_savings_contributions_pa_input ):
        self.max_pension_value_input=max_pension_value_input
        self.planned_ISA_contributions_pa_input=planned_ISA_contributions_pa_input
        self.planned_cash_savings_contributions_pa_input=planned_cash_savings_contributions_pa_input

    def breach_pension_lifetime_allowance(self):
        lifetime_allowance=1073000
        excess_over_lifetime_allowance=self.max_pension_value_input-lifetime_allowance
        Tax_rate=0.55
        if excess_over_lifetime_allowance>0:
            return "It looks like you will breach the lifetime allowance by approximately £"+str(self.max_pension_value_input-lifetime_allowance)+'.  This could cost you potentially £'+str(round(excess_over_lifetime_allowance*Tax_rate))+" in additional tax."

    def not_maxing_ISA(self):
        isa_allowance=20000
        if self.planned_ISA_contributions_pa_input !=None:
            if self.planned_ISA_contributions_pa_input<isa_allowance:
                additional_potential_ISA_contributions= min(isa_allowance-self.planned_ISA_contributions_pa_input,    self.planned_cash_savings_contributions_pa_input )
                return "You could contribute another £"+str(additional_potential_ISA_contributions)+" to your ISA each year.  This will allow you to avoid paying tax on interest or any capital gain"

    Insight_catalogue = [breach_pension_lifetime_allowance, not_maxing_ISA]

    def extract_insight_list(self):
        Insights_list=[]

        for f in self.Insight_catalogue:
            if f(self) != None:
                Insights_list.append(f(self))
        return Insights_list





