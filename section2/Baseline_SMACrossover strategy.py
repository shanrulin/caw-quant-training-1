#!/usr/bin/env python
# coding: utf-8

# In[3]:


# all built-in libraries at the top
import os
import datetime

# all third-party libraries in the middle
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt

# my own modules
from section1_task1 import histohour_data

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
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position.size:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

# fetch data
histohour_data('BTC','USDT','2020-04-01','2020-01-01','binance')
# Move the file by renaming it's path
os.rename('./BTC_USDT_1h.csv', './data/BTC_USDT_1h.csv')

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)

cerebro.adddata(datafeed) # Add the data feed

cerebro.addstrategy(SMACross)  # Add the trading strategy

# additional backtest setting
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# get strategy name, and parameter values
strategy_name=cerebro.strats[0][0][0].__name__
p_pfast = cerebro.strats[0][0][0].params.pfast
p_pslow = cerebro.strats[0][0][0].params.pslow
logfile= datafile.split('.')[0]+'_'+strategy_name+'_'+str(p_pfast)+'_'+str(p_pslow)+'_'+from_datetime.split()[0]+'_'\
        +to_datetime.split()[0]+'.csv'

# add logger
cerebro.addwriter(
    bt.WriterFile, out=os.path.join(logdir, logfile),csv=True)

cerebro.run()  # run it all

# save report
plt.rcParams['figure.figsize'] = [13.8, 10]
fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
figfile= datafile.split('.')[0]+'_'+strategy_name+'_'+str(p_pfast)+'_'+str(p_pslow)+'_'+from_datetime.split()[0]+'_'\
         +to_datetime.split()[0]+'.png'
fig[0][0].savefig(
    os.path.join(reportdir, figfile),
    dpi=480)
