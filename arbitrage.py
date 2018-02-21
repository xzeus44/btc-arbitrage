from zaifapi import *
import pybitFlyer
import configparser
from pprint import pprint

config = configparser.CofigfParser()
config.read('credentials.ini')
# zaif
ZAIF_API_KEY = config['ZAIF']['API_KEY']
ZAIF_API_SECRET = config['ZAIF']['API_SECRET']

zaif = ZaifTradeApi(key=ZAIF_API_KEY, secret=ZAIF_API_SECRET)
zaif_pub = ZaifPublicApi()
zf_price = zaif_pub.ticker('btc_jpy')

# bitFlyer
BITFLYER_API_KEY = config['bitFlyer']['API_KEY']
BITFLYER_API_SECRET = config['bitFlyer']['API_SECRET']
BITFLYER_ADDRESS = config['bitFlyer']['ADDRESS']

bfapi = pybitFlyer.API(api_key=BITFLYER_API_KEY, api_secret=BITFLYER_API_SECRET)

bf_price = bfapi.ticker(product_code='BTC_JPY')


# judge if arbitrage
zf_ask_price = zf_price['ask']
zf_bid_price = zf_price['bid']
bf_ask_price = bf_price['best_ask']
bf_bid_price = bf_price['best_bid']

bid_zf_ask_bf = zf_bid_price < bf_ask_price  # buy at zf. sell at bf
bid_bf_ask_zf = bf_bid_price < zf_ask_price  # buy at bf. sell at zf 
print('Should buy at zif and sell at btf', bid_zf_ask_bf)
print('Should buy at btf and sell at zif', bid_bf_ask_zf)

if bid_zf_ask_bf:
    # buy bitcoin at zaif
    btc_amount = 100 / zf_bid_price
    zf_traded = zaif.trade(currency_pair='btc_jpy',
               action='bid',
               amount=btc_amount,
               price=zf_bid_price + 100)

    pprint(zf_traded)

    # wait until your zaif account if you got bitcoin


    # send bitcoin from zaif to bitFlyer
    zf_withdrew = zaif.withdraw(
            currency='btc',
            address=BITFLYER_ADDRESS,
            amount=btc_amount)

    pprint(zf_withdrew)

if bid_bf_ask_zf:
    btc_amount = 100 / bf_bid_price

    # TODO write code to buy bitcoin
    bf_traded = bfapi.sendchildorder(product_code="BTC_JPY",
		   child_order_type="MARKET",
		   side="BUY",
		   size=btc_amount,
		   minute_to_expire=10000,
		   time_in_force="GTC"
		)

    # TODO write code to send BTC to zaif
    

#zaif = ZaifTradeApi(key, secret)
