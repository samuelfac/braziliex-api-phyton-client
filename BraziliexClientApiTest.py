# -*- coding: utf-8 -*-

import BraziliexClientApi
API_ID = '<API_ID>'
API_SECRET = '<API_SECRET>'

api = BraziliexClientApi.Api()
print (api.currencies())
print (api.ticker())
print (api.ticker(BraziliexClientApi.Market.BTC_BRL))
print (api.orderbook(BraziliexClientApi.Market.BTC_BRL))
print (api.tradehistory(BraziliexClientApi.Market.BTC_BRL))

trader = BraziliexClientApi.Trader(API_ID,API_SECRET)
print (trader.balance())
print (trader.complete_balance())
print (trader.open_orders(BraziliexClientApi.Market.BTC_BRL))
print (trader.trade_history(BraziliexClientApi.Market.BTC_BRL))
print (trader.deposit_address(BraziliexClientApi.Currency.XMR))
print (trader.sell(BraziliexClientApi.Market.BTC_BRL, 1.1, 2.1))
print (trader.buy(BraziliexClientApi.Market.BTC_BRL, 1.1, 2.1))
print (trader.cancel_order(BraziliexClientApi.Market.BTC_BRL, 1234))
