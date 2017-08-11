# -*- coding: utf-8 -*-

import BrazilexClientApi
API_ID = '<API_ID>'
API_SECRET = '<API_SECRET>'

api = BrazilexClientApi.Api()
print (api.currencies())
print (api.ticker())
print (api.ticker(BrazilexClientApi.Market.BTC_BRL))
print (api.orderbook(BrazilexClientApi.Market.BTC_BRL))
print (api.tradehistory(BrazilexClientApi.Market.BTC_BRL))

trader = BrazilexClientApi.Trader(API_ID,API_SECRET)
print (trader.balance())
print (trader.complete_balance())
print (trader.open_orders(BrazilexClientApi.Market.BTC_BRL))
print (trader.trade_history(BrazilexClientApi.Market.BTC_BRL))
print (trader.deposit_address(BrazilexClientApi.Currency.XMR))
print (trader.sell(BrazilexClientApi.Market.BTC_BRL, 1.1, 2.1))
print (trader.buy(BrazilexClientApi.Market.BTC_BRL, 1.1, 2.1))
print (trader.cancel_order(BrazilexClientApi.Market.BTC_BRL, 1234))
