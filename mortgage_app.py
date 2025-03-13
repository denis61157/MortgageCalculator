import streamlit as st
import pandas as pd
import numpy as np


def calculate_mortgage(PropertyPrice, DownPayment, LoanTermYears, Margin, EIBOR_3M, MinRate, FixedRate):
    LoanAmount = PropertyPrice - DownPayment
    LoanTermMonths = LoanTermYears * 12
    remaining_loan = LoanAmount
    payment_schedule = []

    def calculate_annuity_payment(principal, annual_rate, months_remaining):
        monthly_rate = (annual_rate / 100) / 12
        if monthly_rate == 0:
            return principal / months_remaining
        return principal * monthly_rate / (1 - (1 + monthly_rate) ** -months_remaining)

    annual_rate = FixedRate
    for month in range(1, 37):
        monthly_payment = calculate_annuity_payment(remaining_loan, annual_rate, LoanTermMonths - (month - 1))
        interest_payment = (annual_rate / 100 / 12) * remaining_loan
        principal_payment = monthly_payment - interest_payment
        remaining_loan -= principal_payment
        payment_schedule.append(
            [month, monthly_payment, interest_payment, principal_payment, remaining_loan, annual_rate])

    for month in range(37, LoanTermMonths + 1):
        if (month - 1) % 3 == 0:
            annual_rate = max(EIBOR_3M + Margin, MinRate)

        monthly_payment = calculate_annuity_payment(remaining_loan, annual_rate, LoanTermMonths - (month - 1))
        interest_payment = (annual_rate / 100 / 12) * remaining_loan
        principal_payment = monthly_payment - interest_payment
        remaining_loan -= principal_payment
        payment_schedule.append(
            [month, monthly_payment, interest_payment, principal_payment, remaining_loan, annual_rate])

    df = pd.DataFrame(payment_schedule,
                      columns=["Month", "Total Payment", "Interest Payment", "Principal Payment", "Remaining Loan",
                               "Annual Rate"])
    return df


st.title("Dubai Luxury Mortgage Calculator and SPA and Golf")

PropertyPrice = st.number_input("Property Price ($)", min_value=10000, step=10000, value=1150000)
DownPayment = st.number_input("Down Payment ($)", min_value=1000, step=1000, value=230000)
LoanTermYears = st.number_input("Loan Term (years)", min_value=1, step=1, value=25)
Margin = st.number_input("Bank Margin (%)", min_value=0.1, step=0.1, value=1.50)
EIBOR_3M = st.number_input("Initial 3M EIBOR Rate (%)", min_value=0.1, step=0.1, value=4.27)
MinRate = st.number_input("Minimum Rate (%)", min_value=0.1, step=0.1, value=1.99)
FixedRate = st.number_input("Fixed Rate for 3 Years (%)", min_value=0.1, step=0.1, value=3.99)

if st.button("Calculate Mortgage"):
    df = calculate_mortgage(PropertyPrice, DownPayment, LoanTermYears, Margin, EIBOR_3M, MinRate, FixedRate)
    st.write("### Payment Schedule")
    st.dataframe(df)
