import sys
import warnings
import pandas as pd
import numpy as np

transactions_path = "test.csv"

def main(path):
    # Read the amount of points to spend
    if len(sys.argv) == 1:
        warnings.warn("Please provide the amount of points to spend", stacklevel=2)
        sys.exit()
    elif len(sys.argv) > 2:
        warnings.warn("Too many arguments", stacklevel=2)
        sys.exit()
    else:
        points_to_spend = np.int64(sys.argv[-1])
    
    # Load transaction data
    transactions = pd.read_csv(path)

    # 1. Save initial point balances
    # output example:
    # {         
    #   "DANNON":         1100
    #   "MILLER_COORS":   10000
    #   "UNILEVER":       200
    # }
    balances = transactions[['payer', 'points']].groupby('payer').sum().T.to_dict()
    balances = {k: v['points'] for k, v in balances.items()}

    # 2. Sort transactions by datetime 
    transactions['datetime'] = pd.to_datetime(transactions['timestamp'])
    transactions.sort_values(by="datetime", inplace=True)

    # 3. Spend points
    for ind in transactions.index:
        # There is no point to spend 
        if points_to_spend == 0 or sum(balances.values()) == 0:
            break
        
        points_arr = [
            balances[transactions['payer'][ind]],   # 1 payer's total point balance
            transactions['points'][ind],            # 1 payer's 1 transaction points  
            points_to_spend                         # Total points to spend left
        ]

        # Subtract each of the above by the smallest one
        # 3.1 If points_to_spend is the smallest, then we just spend all the points.
        # 3.2 If a single transaction's points is the smallest, then we spend all its points.
        # 3.3 If a payer's point balances is the smallest, then we spend to make the balance 0. 
        smallest_points = points_arr[np.argmin(points_arr)]
        points_to_spend -= smallest_points
        transactions.at[ind, 'points'] -= smallest_points 
        balances[transactions['payer'][ind]] -= smallest_points

    print("payers point balances: ", balances)
    # print("\npoints to spend left:", points_to_spend)
    # print("\ntransaction points balances:\n", transactions)


if __name__=="__main__":
    main(transactions_path)