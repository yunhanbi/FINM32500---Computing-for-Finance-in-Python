# README

## Future Improvement

In this competition, we've encountered two issues that could be improved in the future. 
(1) On the first day, some of our code didn't work perfectly with API. So we used first day to debug. In the future, such foreward testing could be done before real time implementation. 

(2) Our Alpaca paper trading account was locked on Thursday, leading us unable to liquidate our positions or make new orders on Thursday afternoon and Friday. After investigating the issues, we believe that this is caused by the race condition that first makes the orders pending and then lead to a internal lock in api. This could be due to either the trade interval is too short or connection lag. We could expand the trading interval and also add logic to place new order only when the old order is completed to solve this problem in the future.

## Python Version

In the python file, we've used Numpy == 2.4.1 and Pandas == 2.3.3.

## Parameters

We've put the parameters in main.py so that each aspects can be modified accordingly.

## Execution

To run the whole Algorithm, please put all python file under the same folder directory, make sure the Numpy and Pandas version are correct and then run the main.py. 
main.py will run the algo and save the results into 'final_report.csv', then using performance.ipynb will generate the performance md file report.