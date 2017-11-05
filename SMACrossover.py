from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume
from quantopian.pipeline.filters.morningstar import Q500US
 
def initialize(context):
    """
    Called once at the start of the algorithm.   
    """       
    context.security = symbol('SPY')
 
def handle_data(context,data):
    """
    Called every minute.
    """
    
    print(data)
    
    """
    Moving averages Algorithm, This compares a short term moving average against a long term moving average, and the point in which MA1 (short term)                 curve crosses above MA2(longterm) It is a buy point, and when it falls under it is a sell point. 
    
    Thank you, 
    Abhishek Mahesh    
    """
    
    MA1 = data.history(context.security,"price",bar_count=50, frequency = "1d").mean()
    MA2 = data.history(context.security,"price",bar_count=200, frequency = "1d").mean()


    
    current_price = data.current(context.security,"price")
    current_positions = context.portfolio.positions[symbol('SPY')].amount
    cash = context.portfolio.cash
    
    
    if (MA1 > MA2) and current_positions == 0:

        numberOfShares  = int(cash/current_price)
        order(context.security, numberOfShares)
        log.info('buying shares')        
    elif (MA1<MA2) and current_positions != 0:
        #order_target is a target number of shares
        order_target(context.security, 0)
        log.info('selling shares')
    
    record(MA1 = MA1, MA2 = MA2, Price = current_price)

