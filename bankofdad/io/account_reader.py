# Standard library imports
from datetime import date

# Math imports
from numpy import genfromtxt
# ETS imports

# Local imports
from bankofdad.model.account import Account
from bankofdad.model.transaction import Transaction


def load_account_from_csv(filename):
    """ Read an account from a CSV file
    """
    dt = [('Date', "S10"), ('Action', 'S9'), ('Amount', 'S6'),
          ('Balance', 'S6'), ('comment', 'S24'), ('f1', '<f8'), ('f2', '<f8')]
    data = genfromtxt(filename, dtype=dt, comments="#", delimiter="\t",
                      skip_header=1)
    transactions = []
    for trans in data:
        mm, dd, yy = trans["Date"].split("/")
        if trans["Action"].lower().startswith("withdraw"):
            kind = "withdrawal"
        elif trans["Action"].lower().startswith("allow"):
            kind = "allowance"
        elif trans["Action"].lower().startswith("inter"):
            kind = "interest"
        elif trans["Action"].lower().startswith("dep"):
            kind = "deposit"
        transactions.append(
            Transaction(
                time_stamp=date(int(yy), int(mm), int(dd)),
                amount=float(trans["Amount"].replace("$", "")),
                kind=kind, comment=str(trans["comment"]),
                ))
    account = Account(
        transactions=transactions,
    )
    return account
