#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### Task3 Optimize Parameter in Strategy


# In[26]:


# all built-in libraries 
import os
import datetime

# all third-party libraries in the middle
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import backtrader.analyzers as btanalyzers

# declare all environment params / global variables.
datadir = './data' # data path
logdir = './log' # log path
reportdir = './report' # report path
datafile = 'BTC_USDT_1h.csv' # data file
from_datetime = '2020-01-01 00:00:00' # start time 
to_datetime = '2020-04-01 00:00:00' # end time

# Create a subclass of Strategy to define the indicators and logic

class SMACross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = (
        ('pfast', 10),  # period for the fast moving average
        ('pslow', 20),  # period for the slow moving average
        ('printlog', False),                                
    )
    
    ## keep log
    def log(self, txt, dt=None, doprint=False):              
        ''' Logging function fit this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))    
    
    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        
        # skip unwanted pairs
        if self.p.pfast > self.p.pslow:
            raise bt.StrategySkipError
        
    def next(self):
        if not self.position.size:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
    
    ## get ending value at the end of datafeed
    def stop(self):                                                          
        self.log('pfast {}, pslow {}, Ending Value {:.2f}'.format
                 (self.params.pfast, self.params.pslow, self.broker.getvalue()), doprint=True)

        
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a datafeed
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)

cerebro.adddata(datafeed) # Add the data feed

# Add a strategy
strats = cerebro.optstrategy(SMACross, pfast=range(5, 21), pslow=range(10, 51))   


# add annual return Analyzer
cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='my_annualreturn')
# add DrawDown analyzer
cerebro.addanalyzer(btanalyzers.DrawDown, _name='my_drawdown')
# add TradeAnalyzer Analyzer
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='mytrade')


# additional backtest setting
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

results=cerebro.run(maxcpus=1)  # run it all


# In[27]:


#print(len(results)) # StrategySkipError skip the unwanted pairs, but cerebro still save a space for it


# In[28]:


## get strategy name
strategy_name = results[0][0].strategycls.__name__

## build an empty dataframe
df = pd.DataFrame(columns =
                  ('Name','sma_pfast', 'sma_pslow', 'Return','MaxDrawDown', 'TotalTrades#',\
                   'WinTrades#', 'LossTrades#', 'WinRatio', 'AverageWin$', 'AverageLoss$', 'AverageWinLossRatio'))

## store KPI in the dataframe
for i in range(len(results)):
    
    ## skip empty result
    if len(results[i]) == 0:
        continue
    
    ## get all required KPI
    sma_pfast = results[i][0].p.pfast
    sma_pslow = results[i][0].p.pslow
    Return = results[i][0].analyzers.my_annualreturn.get_analysis()[2020]
    MaxDrawDown = results[i][0].analyzers.my_drawdown.get_analysis()['max']['drawdown']
    
    trade_num = results[i][0].analyzers.mytrade.get_analysis()['total']['total']
    ## make sure that there is trade data
    if trade_num != 0:
        TotalTrades = results[i][0].analyzers.mytrade.get_analysis()['total']['closed'] 
        win_t = results[i][0].analyzers.mytrade.get_analysis()['won']['total']
        lost_t = results[i][0].analyzers.mytrade.get_analysis()['lost']['total']
        win_ratio = win_t/TotalTrades
        avg_win = results[i][0].analyzers.mytrade.get_analysis().won.pnl.average
        avg_lost = results[i][0].analyzers.mytrade.get_analysis().lost.pnl.average
        avg_winlost = avg_win/avg_lost
    
    ## if trade_num = 0, there is no data for win/lost trade
    else:
        TotalTrades = 0
        win_t = 0
        lost_t = 0
        win_ratio = 0
        avg_win = 0
        avg_lost = 0
        avg_winlost = 0
    
    df.loc[i] = [strategy_name, sma_pfast, sma_pslow, Return, MaxDrawDown, TotalTrades,                win_t, lost_t, win_ratio, avg_win, avg_lost, avg_winlost]


# In[29]:


df.reset_index(drop=True, inplace=True)


# In[31]:


## Compute rank of 4 KPIs
# -Rank of Return
# -Rank of Maxdrawdown (the maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained)
# -Rank of WinLossRatio
# -Rank of AverageWinLossRatio
df['RankReturn'] = df['Return'].rank(ascending=False)
df['RankMaxDrawDown'] = df['MaxDrawDown'].rank()
df['RankWinRatio'] = df['WinRatio'].rank(ascending=False)
df['RankAverageWinLossRatio'] =df['AverageWinLossRatio'].rank(ascending=False)


## Compute score(average of 4 Ranks)
df['Score'] = df[['RankReturn', 'RankMaxDrawDown', 'RankWinRatio', 'RankAverageWinLossRatio']].mean(axis=1)


# In[33]:


## get the index of the winner, which is the smallest score
df['Score'].idxmin()

# conclusion: the winner has pfast 16 and pslow 25


# In[35]:


## save dataframe to csv
df.to_csv ('BTC_USDT_1h_SMACross.csv', index = True, header=True)

