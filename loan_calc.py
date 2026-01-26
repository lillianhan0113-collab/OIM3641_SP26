import math

def calculate_loan_payment(interest, term, present_value):
    """
    Calculates the monthly loan payment using the standard loan payment formula.

    Args:
        interest (float): The annual interest rate (e.g., 0.05 for 5%).
        term (int): The term of the loan in years.
        present_value (float): The principal loan amount (present value).

    Returns:
        float: The monthly loan payment. Returns float('inf') for invalid inputs
               where a non-zero loan would have an undefined or infinite payment
               (e.g., zero term for non-zero present value).
               Returns 0.0 if present_value is 0 or term is <=0 and present_value is 0.
    """
    if present_value < 0:
        # A loan amount (present value) is typically non-negative.
        # If it were negative, the payment would also be negative (money paid to borrower).
        # We will proceed with the calculation, but semantically, a negative PV is unusual for a loan payment.
        pass

    if term <= 0:
        if present_value == 0:
            return 0.0  # No loan, no payment
        else:
            # Cannot pay back a non-zero loan in zero or negative time.
            # This implies an infinite payment.
            return float('inf')

    # Convert annual interest rate to a monthly rate
    monthly_interest_rate = interest / 12

    # Calculate the total number of payments
    number_of_payments = term * 12

    if monthly_interest_rate == 0:
        # Special case for zero interest: simple division of principal by total number of payments
        return present_value / number_of_payments
    else:
        # Standard loan payment formula: M = P [ r(1 + r)^n ] / [ (1 + r)^n – 1]
        # P = present_value
        # r = monthly_interest_rate
        # n = number_of_payments

        # Calculate (1 + r)^n
        pow_val = (1 + monthly_interest_rate)**number_of_payments

        numerator = monthly_interest_rate * pow_val
        denominator = pow_val - 1
        
        # Guard against potential floating point inaccuracies if denominator becomes extremely small
        # (this would happen if monthly_interest_rate is very close to zero but not exactly zero)
        if abs(denominator) < 1e-9: # A small threshold to consider it effectively zero
            return present_value / number_of_payments

        monthly_payment = present_value * (numerator / denominator)
        return monthly_payment