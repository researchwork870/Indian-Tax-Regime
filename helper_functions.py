"""This module defines all the functions for tax analysis"""


def calculate_tax(income : float, regime : str, age : int) -> float :
    """
    Calculates income tax using different regimes for all individuals.

    Inputs:
         income : Gross Income - Employer's PF - gratuity
         regime : "old"   - traditional scheme
                  "new"   - tax regime introduced in budget 2020
                  "newer" - tax regime introduced in budget 2023
         age    : Age of the taxpayer. Tax slabs differ under old regime for different age groups 
    Output:
        income tax 
    """
    if regime == "old":
        standard_deduction = 50000 # This is provided in old regime
        taxable_income = income - standard_deduction  # standard deduction under old regime
        
        if age < 60:
            slabs = [
            (250000, 0, 0.0),   # No tax up to Rs. 2.5 lakh
            (500000, 250000, 0.05),  # 5% tax on income between Rs. 2.5 lakh to Rs. 5 lakh
            (1000000, 500000, 0.2),  # 20% tax on income between Rs. 5 lakh to Rs. 10 lakh
            (float('inf'), 1000000, 0.3)  # 30% tax on income above Rs. 10 lakh
            ]
        elif age >= 60 and age < 80:
            slabs = [
            (300000, 0, 0.0),   # No tax up to Rs. 3 lakh
            (500000, 300000, 0.05),  # 5% tax on income between Rs. 2.5 lakh to Rs. 5 lakh
            (1000000, 500000, 0.2),  # 20% tax on income between Rs. 5 lakh to Rs. 10 lakh
            (float('inf'), 1000000, 0.3)  # 30% tax on income above Rs. 10 lakh
            ]
        elif age >= 80:
            slabs = [
            (500000, 0, 0.0),   # No tax up to Rs. 5 lakh
            (1000000, 500000, 0.2),  # 20% tax on income between Rs. 5 lakh to Rs. 10 lakh
            (float('inf'), 1000000, 0.3)  # 30% tax on income above Rs. 10 lakh
            ]

    elif regime == "new":
        standard_deduction = 0 # No standard deduction
        taxable_income = income  # No standard deduction is provided

        slabs = [
        (250000, 0, 0.0),   # No tax up to Rs. 2.5 lakh
        (500000, 250000, 0.05),  # 5% tax on income between Rs. 2.5 lakh to Rs. 5 lakh
        (750000, 500000, 0.1),  # 10% tax on income between Rs. 5 lakh to Rs. 7.5 lakh
        (1000000, 750000, 0.15),  # 15% tax on income between Rs. 7.5 lakh to Rs. 10 lakh
        (1250000, 1000000, 0.2),  # 20% tax on income between Rs. 10 lakh to Rs. 12.5 lakh
        (1500000, 1250000, 0.25),  # 25% tax on income between Rs. 12.5 lakh to Rs. 15 lakh
        (float('inf'), 1500000, 0.3)  # 30% tax on income above Rs. 15 lakh
        ]

    elif regime == "newer":
        standard_deduction = 50000 # This is provided in 2023 introduced new regime. 
        taxable_income = income - standard_deduction  # standard deduction under 2023 new tax regime

        slabs = [
        (300000, 0, 0.0),   # No tax up to Rs. 3 lakh
        (600000, 300000, 0.05),  # 5% tax on income between Rs. 3 lakh to Rs. 6 lakh
        (900000, 600000, 0.1),  # 10% tax on income between Rs. 6 lakh to Rs. 9 lakh
        (1200000, 900000, 0.15),  # 15% tax on income between Rs. 9 lakh to Rs. 12 lakh
        (1500000, 1200000, 0.2),  # 20% tax on income between Rs. 12 lakh to Rs. 15 lakh
        (float('inf'), 1500000, 0.3)  # 30% tax on income above Rs. 15 lakh
        ]
        if taxable_income <= 700000:
            return 0

    slab_tax = []

    # Calculate tax
    tax = 0.0
    for i, (slab_ceiling, slab_floor, slab_rate) in enumerate(slabs):
        if taxable_income <= slab_ceiling:
            tax += (taxable_income - slab_floor) * slab_rate
            slab_tax.append((taxable_income - slab_floor) * slab_rate)
            break
        else:
            tax += (slab_ceiling - slab_floor) * slab_rate
            slab_tax.append((slab_ceiling - slab_floor) * slab_rate)

    #print(f"Total income tax with income Rs. {income:.2f} is Rs. {tax:.2f} \n Tax summary {slab_tax}")
    return tax


def calculate_surcharge(income : float, regime : str, age : int) -> float:
    """
    Calculates surcharge for incomes using different regimes for all individuals.

    Inputs:
         taxable_income : Gross Income - Employer's PF - gratuity - standard deduction (applicable as per regimes)
         income : Gross Income - Employer's PF - gratuity
         regime : "old"   - traditional scheme
                  "new"   - tax regime introduced in budget 2020
                  "newer" - tax regime introduced in budget 2023
         age    : Age of the taxpayer. Tax slabs differ under old regime for different age groups 
    Output:
        surcharge 
    """
    if regime == "newer":
        standard_deduction = 50000 # This is provided in 2023 introduced new regime. 
        taxable_income = income - standard_deduction  # standard deduction under 2023 new tax regime

        surcharge_rates = [(5000000, 10000000, 0.1),   
                       (10000000, 20000000, 0.15),    
                       (20000000, float('inf'), 0.25)]
    
    elif regime == "new":
        standard_deduction = 0 # No standard deduction
        taxable_income = income  # No standard deduction is provided

        surcharge_rates = [(5000000, 10000000, 0.1),
                       (10000000, 20000000, 0.15),
                       (20000000, 50000000, 0.25),
                       (50000000, float('inf'), 0.37)]
    
    elif regime == "old":
        standard_deduction = 50000 # This is provided in old regime
        taxable_income = income - standard_deduction  # standard deduction under old regime

        surcharge_rates = [(5000000, 10000000, 0.1), 
                       (10000000, 20000000, 0.15),   
                       (20000000, 50000000, 0.25),
                       (50000000, float('inf'), 0.37)]
        
    if taxable_income <= 5000000: # surcharge not applicable
        return 0

        
    for _, (slab_floor, slab_ceil, surcharge_rate) in enumerate(surcharge_rates):
        if taxable_income > slab_floor and taxable_income <= slab_ceil:
            lower_bound = slab_floor
            rate = surcharge_rate

    # This dictionary is used to calculate tax liability including surcharge for income at slab levels (where one slab ends and other starts)
    applicable_surcharge_rate = {5000000 : 0,
                                 10000000 : 0.1,
                                 20000000 : 0.15,
                                 50000000 : 0.25}
            
    total_tax = calculate_tax(income, regime, age) * (1 + rate)
    lower_bound_income_total_tax = calculate_tax(lower_bound + standard_deduction, regime, age) * (1 + applicable_surcharge_rate[lower_bound])
    
    # If additional tax applicable is greater than additional income earned then marginal relief is applicable  
    if total_tax -  lower_bound_income_total_tax > taxable_income - lower_bound:
        marginal_relief = total_tax -  lower_bound_income_total_tax - (taxable_income - lower_bound)
        tax_after_marginal_relief = total_tax - marginal_relief
        surcharge = tax_after_marginal_relief - calculate_tax(income, regime, age)
        #print(f'Income :{taxable_income} Surcharge :{surcharge} marginal_relief: {marginal_relief}')
        return surcharge
    else:
        return calculate_tax(income, regime, age) * rate

def calculate_total_tax(income : float, regime : str, age : int) -> float:
    """ Calculates total tax on income"""

    return (calculate_tax(income, regime, age) + calculate_surcharge(income, regime, age)) * 1.04 # health and education cess

def calculate_income_old_regime(tax : float) -> float:
    """
    This function calculates the inverse of calculate_income_tax(income, "old") function
    It takes in income tax and returns income

    
    Mathematical technicality:
    
    tax = 0 is not included in the domain of this function because the calculate_income_tax(income, "old") function
    is not one-one. For example:
    
    calculate_income_tax(200000, "old") = 0
    calculate_income_tax(250000, "old") = 0

    Therefore, calculate_income_tax(income, "old") function is not invertible in the domain -> [0, 300000]
    """
    tax = tax/1.04
    if tax == 0:
        return "Anywhere between 0 and 300000"
    elif 0 < tax <= 12500:
        income = tax / 0.05 + 300000 # (300000 = 250000 + 50000 -> income ceil in first slab + standard deduction)
        return income 
    elif 12500 < tax <= 112500:
        income = (tax - 12500) / 0.2 + 550000 # (550000 = 500000 + 50000 -> income ceil in second slab + standard deduction)
        return income
    elif 112500 < tax <= 1312500:
        income = (tax - 112500) / 0.3 + 1050000 # (1050000 = 1000000 + 50000 -> income ceil in third slab + standard deduction)
        return income
    elif 1312500 < tax <= 1508395.5223000003:
        income = (tax - 1312500) + 5050000   # due to surcharge marginal relief is applicable and all the income is contributed in tax
        return income
    elif 1508395.5223000003 < tax <= 3093750:
        income = (tax/1.1 - 112500) / 0.3 + 1050000 # dividing it by surcharge of 10% and then finding the income
        return income
    elif 3093750 < tax <= 3308444.6564925:
        income = (tax - 3093750) + 10050000  # due to surcharge marginal relief is applicable and all the income is contributed in tax
        return income
    elif 3308444.6564925 < tax <= 6684375:
        income = (tax/1.15 - 112500) / 0.3 + 1050000 # dividing it by surcharge of 15% and then finding the income
        return income
    elif 6684375 < tax <= 7614375:
        income = (tax - 6684375) + 20050000  # due to surcharge marginal relief is applicable and all the income is contributed in tax
        return income
    elif 7614375 < tax <= 18515625:
        income = (tax/1.25 - 112500) / 0.3 + 1050000 # dividing it by surcharge of 25% and then finding the income
        return income
    elif 18515625 < tax <= 21533451.825:
        income = (tax - 18515625) + 50050000  # due to surcharge marginal relief is applicable and all the income is contributed in tax
        return income
    elif tax > 21533451.825:
        income = (tax/1.37 - 112500) / 0.3 + 1050000 # dividing it by surcharge of 37% and then finding the income
        return income
    
def minimum_exemption_for_tax_regime_equivalence(income : float, regime : str, age : int) -> float:
    """ 
    minimum exemption required after excluding standard deduction is given by:
    N(.) -> function to calculate income tax using new regime 
    O(.) -> function to calculate income tax using old regime

    -> N(I) = O(I-E)
    
    let function Q(.) be inverse of O(.) Therefore,
    E = I - Q(N(I))
    """
    return income - calculate_income_old_regime(calculate_total_tax(income, regime, age))
