import math

def calculate_loan_payment(present_value: float, annual_interest_rate: float, term_years: int) -> float:
    """
    Calculates the fixed monthly payment for a loan.

    Args:
        present_value (float): The principal loan amount (P).
        annual_interest_rate (float): The annual interest rate (e.g., 0.05 for 5%).
        term_years (int): The loan term in years.

    Returns:
        float: The calculated monthly loan payment.
               Returns 0.0 if the term_years is 0, as there's no payment period.
    """
    if term_years <= 0:
        return 0.0

    # Assume monthly payments
    payments_per_year = 12
    
    # Calculate periodic interest rate
    # If annual_interest_rate is 0, avoid division by zero in the formula's denominator
    if annual_interest_rate == 0:
        # In this case, the payment is simply the principal divided by the total number of payments
        total_payments = term_years * payments_per_year
        if total_payments == 0:
            return 0.0
        return present_value / total_payments
    
    periodic_interest_rate = annual_interest_rate / payments_per_year
    
    # Calculate total number of payments
    total_payments = term_years * payments_per_year
    
    # Calculate the payment using the loan payment formula (PMT)
    # PMT = [P * r * (1 + r)^n] / [(1 + r)^n – 1]
    numerator = periodic_interest_rate * math.pow(1 + periodic_interest_rate, total_payments)
    denominator = math.pow(1 + periodic_interest_rate, total_payments) - 1
    
    payment = present_value * (numerator / denominator)
    
    return payment

if __name__ == '__main__':
    # Example Usage:
    # Loan for $100,000 at 5% annual interest over 30 years
    loan_amount = 100000
    annual_rate = 0.05
    loan_term = 30
    
    monthly_payment = calculate_loan_payment(loan_amount, annual_rate, loan_term)
    print(f"Loan Amount: ${loan_amount:,.2f}")
    print(f"Annual Interest Rate: {annual_rate * 100:.2f}%")
    print(f"Loan Term: {loan_term} years")
    print(f"Monthly Payment: ${monthly_payment:,.2f}") # Expected: $536.82

    # Example with different values
    loan_amount_2 = 25000
    annual_rate_2 = 0.035
    loan_term_2 = 5
    monthly_payment_2 = calculate_loan_payment(loan_amount_2, annual_rate_2, loan_term_2)
    print(f"\nLoan Amount: ${loan_amount_2:,.2f}")
    print(f"Annual Interest Rate: {annual_rate_2 * 100:.2f}%")
    print(f"Loan Term: {loan_term_2} years")
    print(f"Monthly Payment: ${monthly_payment_2:,.2f}") # Expected: $454.73

    # Example with zero interest rate
    loan_amount_3 = 12000
    annual_rate_3 = 0.00
    loan_term_3 = 10
    monthly_payment_3 = calculate_loan_payment(loan_amount_3, annual_rate_3, loan_term_3)
    print(f"\nLoan Amount: ${loan_amount_3:,.2f}")
    print(f"Annual Interest Rate: {annual_rate_3 * 100:.2f}%")
    print(f"Loan Term: {loan_term_3} years")
    print(f"Monthly Payment: ${monthly_payment_3:,.2f}") # Expected: $100.00 (12000 / (10 * 12))

    # Example with zero term
    loan_amount_4 = 5000
    annual_rate_4 = 0.04
    loan_term_4 = 0
    monthly_payment_4 = calculate_loan_payment(loan_amount_4, annual_rate_4, loan_term_4)
    print(f"\nLoan Amount: ${loan_amount_4:,.2f}")
    print(f"Annual Interest Rate: {annual_rate_4 * 100:.2f}%")
    print(f"Loan Term: {loan_term_4} years")
    print(f"Monthly Payment: ${monthly_payment_4:,.2f}") # Expected: $0.00