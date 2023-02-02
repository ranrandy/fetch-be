# Backend Take Home Test - Fetch

## Requirements
The code has been tested on Mac, with the following:

- [Python >= 3.8.8](https://www.python.org/downloads/)
- NumPy >= 1.20.2
- pandas >= 1.3.4

<!-- - [NumPy >= 1.20.2](https://numpy.org/install/)
- [pandas >= 1.3.4](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) -->

You can install Python from the above link, and install NumPy and pandas using the following command:

```
pip install numpy pandas
```

## Run the code
1. Replace the `transaction_path` with your own .csv file
2. In your command line, type the following and run.
    ```
    python main.py 5000
    ```
    Replace `5000` with other amount of points to test the code

## Well, this is a failure

What went well: 

- Code is fairly well laid out and commented.
- Works for the provided example - gives the correct answer
- Requesting to spend more points that are available does not drive point totals negative. Consider whether or not this is an error condition that should be flagged.
What could have gone better: 

No unit tests.
Validation
Does not trap and handle non-numeric point input: "python main.py xxx" gives back a stack crawl.
Can spend negative points to increase balance
Negative transaction timestamps not taken into consideration - not spending the oldest points first.
-200 DANNON should leave 100 points available for DANNON initially, but we can spend up to 300 before taking away from UNILEVER
-200 point transaction for DANNON is incorrectly attributed to MILLER COORS after sufficient spending

Consider this input:
"payer","points","timestamp"
"PAYER-A",100,"2023-01-01T15:00:00Z"
"PAYER-A",-50,"2023-01-02T15:00:00Z"
"PAYER-B",200,"2023-01-03T15:00:00Z"
"PAYER-A",50,"2023-01-04T15:00:00Z"
The correct result is {'PAYER-A': 50, 'PAYER-B': 175} but the submission returns {'PAYER-A': 25, 'PAYER-B': 200}.  
There 100 - 50 points from the PAYER-A 01/01/2023 bucket available to spend first, leaving 25 to spend from PAYER-B. The 1/4/2023 PAYER-A points remain unspent.
