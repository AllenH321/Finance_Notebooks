# Import
import pandas as pd


def annuity_payment(pv: float, r: float, n: int) -> float:
    """
    Fixed payment for an ordinary annuity
    pv: present value/principal
    r = periodic effective interest rate
    n: number of periods
    """
    if n <= 0:
        raise ValueError("n must be a positive integer.")
    if r == 0:
        return pv / n
    return pv * r / (1 - (1 + r) ** (-n))


def amortization_schedule(pv: float, r: float, n: int) -> pd.DataFrame:
    """
    Build an amortization schedule table:
    Year, Payment, Interest Paid, Principal Paid, Balance | CumPrincipal, CumInterest
    """
    payment = annuity_payment(pv, r, n)
    balance = pv
    cum_principal = 0.0
    cum_interest = 0.0

    rows = []
    rows.append({
        "Years": 0,
        "Payment": 0.0,
        "Int_Part": 0.0,
        "P_Part": 0.0,
        "Bal_Left": balance,
        "Cum_P": 0.0,
        "Cum_Int": 0.0
    })

    for year in range(1, n + 1):
        interest_part = balance * r
        principal_part = payment - interest_part
        balance -= principal_part

        # numerical cleanup so late balance doesn't show -0.00
        if abs(balance) < 1e-9:
            balance = 0.0

        cum_principal += principal_part
        cum_interest += interest_part

        rows.append({
            "Years": year,
            "Payment": payment,
            "Int_Part": interest_part,
            "P_Part": principal_part,
            "Bal_Left": balance,
            "Cum_P": cum_principal,
            "Cum_Int": cum_interest
        })

    df = pd.DataFrame(rows)

    return df
