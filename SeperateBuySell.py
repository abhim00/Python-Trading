import scipy
import numpy
import math

price_list = []
volume_list = []
bvpin_list = []

previous_price = 0
barriermod = 1.1
plist_len = 30  #list length variable
bvlist_len = 30 #list length variable



# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
    context.SnP = symbol('NRG')


# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    
    #define some variables right quick:
    SandP = context.SnP
    SandP_data = data[SandP]
    current_price = SandP_data.price
    current_volume = SandP_data.volume
    cash = context.portfolio.cash
    
    #curate the lists
    price_and_volume_list_curate(current_price, current_volume, plist_len)

    #check the length of price_list. If it's greater than the length variable, run the classify function.
    if len(price_list) >= plist_len:
        #calculate weighted average and weighted STD based on price and bvpin
        #using volumes as the weights
        average_price, sdev_price = weighted_avg_and_std(price_list, volume_list)
        print(sdev_price)
        #run the meat of the program, which classifies order volume into buy and sell vol.s
        v_buy, v_sell, bvpin = bulk_classify(current_price, previous_price, current_volume, sdev_price)
        #curate the bvpin list
        bvpin_list_curate(bvpin, bvlist_len)

        #calculate the average bvpin
        if len(bvpin_list) >= bvlist_len:
            #capture the last part of the volume list and store it as a new list
            #just capture the last (bvlist_len) variables, though
            bvolume_list = volume_list[(plist_len - bvlist_len):plist_len]
            #figure out your average bvpin
            average_bvpin, sdev_bvpin = weighted_avg_and_std(bvpin_list, bvolume_list)
            
                       
            
                #if there are open orders, don't do anything yet
            if get_open_orders():  
                return
                
            #if the buy/sell ratio is under (value), then sell
            elif bvpin <= (average_bvpin):
                #set up number of shares to sell
                number_of_shares = context.portfolio.positions[SandP.sid].amount
                #sell the shares already
                order(SandP, -number_of_shares)
            #if the buy/sell ratio is over (value), then buy
            elif bvpin > (average_bvpin):
               #find the number of shares hurry up and do it
                number_of_shares = int(cash/current_price)
                #just do it already buy stock  >:|
                order_target_percent(SandP, 1)
    
    
#==========================================================================================
def price_and_volume_list_curate(current_price, current_volume, n):
    #curates the price and volume lists, and n is the global list length
    global previous_price
    
    #if price list or volume list isn't long enough, add values to the list
    if len(price_list) < n or len(volume_list) < n:
        price_list.append(current_price)
        volume_list.append(current_volume)
    else:
        #if the lists are long enough, add values then delete the first value
        price_list.append(current_price)
        volume_list.append(current_volume)
        del price_list[0]
        del volume_list[0]
        previous_price = int(price_list[(n-2)])
    
    return previous_price

#==========================================================================================
def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    
    average = numpy.average(values, weights=weights)
    variance = numpy.average((values-average)**2, weights=weights)  # Fast and numerically precise
    sdev = math.sqrt(variance)
    return average, sdev
#==========================================================================================
def bvpin_list_curate(bvpin, n):
     #if bvpin list isn't long enough, add values to the list. n is the global list length.
    if len(bvpin_list) < n:
        bvpin_list.append(bvpin)
    else:
        #if the lists are long enough, add bvpin to the end then delete the first value
        bvpin_list.append(bvpin)
        del bvpin_list[0]    
    return previous_price
#==========================================================================================    
def bulk_classify(current_price, previous_price, current_volume, sdev_price):  
    """  
    p: prices  
    v: volumes  
    """  
    
    #price difference
    dprice = current_price - previous_price
    #volume call
    volume = current_volume
    #buy volume = volume call times Z times dprice over standard deviation of the price diff
    if sdev_price == 0:
        sdev_price = 1
    v_buy = volume * scipy.stats.norm.cdf(dprice / sdev_price)  
    #v sell
    v_sell = volume - v_buy  
    
    #percentage of buy volume maybe?
    bvpin = (v_buy - v_sell) / volume  
    
    return v_buy, v_sell, bvpin