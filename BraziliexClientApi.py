# -*- coding: utf-8 -*-

import hashlib
import hmac
import http.client
import json
import urllib
import time

import urllib.request

from enum import Enum
from collections import OrderedDict

REQUEST_HOST = 'braziliex.com'
TRADER_REQUEST_PATH = '/api/v1/private/'
API_REQUEST_PATH = '/api/v1/public/'

class Market(Enum):
    LTC_BTC = 'ltc_btc'
    ETH_BTC = 'eth_btc'
    XMR_BTC = 'xmr_btc'
    DASH_BTC = 'dash_btc'
    BTC_BRL = 'btc_brl'
    ETH_BRL = 'eth_brl'
    LTC_BRL = 'ltc_brl'
    XMR_BRL = 'xmr_brl'
    DASH_BRL = 'dash_brl'
    PRSP_BTC = 'prsp_btc'
    MXT_BTC = 'mxt_btc'

class Currency(Enum):
    BRL	 = 'brl'
    BTC	 = 'btc'
    DASH = 'dash'
    ETH	 = 'eth'
    LTC	 = 'ltc'
    MXT	 = 'mxt'
    PRSP = 'prsp'
    XMR	 = 'xmr'


class Api():
    '''API Reference v1
Brazilex
https://braziliex.com/exchange/api.php'''
    
    def __get(self, method, nomeRetorno = ''):
        req = urllib.request.Request('https://'+REQUEST_HOST + API_REQUEST_PATH + method)
        req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5')
        r = urllib.request.urlopen(req).read()
        # É fundamental utilizar a classe OrderedDict para preservar a ordem dos elementos
        response_json = json.loads(r.decode('utf-8'), object_pairs_hook=OrderedDict)

        if(nomeRetorno and nomeRetorno!=''):
            return json.dumps(response_json[nomeRetorno], indent=4)
        else:
            return json.dumps(response_json, indent=4)


    def currencies(self):
        '''Used to get the open and available trading markets at Braziliex along with other meta data.'''
        return self.__get('currencies')
    
    def ticker(self):
        '''Used to get the last 24 hour summary of all active exchanges.'''
        return self.__get('ticker')
    
    def ticker_market(self, market):
        '''Used to get the current tick values for a market.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')

        return self.__get('ticker/'+market.value)
    
    def orderbook(self, market):
        '''Used to get retrieve the orderbook for a given market.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')

        return self.__get('orderbook/'+market.value)
    
    def tradehistory(self, market):
        '''Used to get retrieve the last 15 trades.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')

        return self.__get('tradehistory/'+market.value)
    


class Trader():
    '''Brazilex
https://braziliex.com/exchange/api.php

To use the private API, you will need to create an API key (https://braziliex.com/exchange/api_key.php).'''
    
    def __init__(self, MB_TAPI_ID, MB_TAPI_SECRET):
        self.MB_TAPI_ID = MB_TAPI_ID
        self.MB_TAPI_SECRET = MB_TAPI_SECRET

    def __post(self, method, params, nomeRetorno = ''):
        params['command'] = method
        # Nonce
        # Para obter variação de forma simples
        # timestamp pode ser utilizado:
        nonce = int(time.time()*1000)
        #nonce = 1
        params['nonce'] = nonce
        params = urllib.parse.urlencode(params)

        # Gerar MAC
        params_string = TRADER_REQUEST_PATH + '?' + params
        H = hmac.new(bytearray(self.MB_TAPI_SECRET.encode()), digestmod=hashlib.sha512)
        H.update(params.encode())
        tapi_mac = H.hexdigest()
        
        # Gerar cabeçalho da requisição
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Key': self.MB_TAPI_ID,
            'Sign': tapi_mac
        }
        
        # Realizar requisição POST
        conn = ''
        try:
            conn = http.client.HTTPSConnection(REQUEST_HOST)
            conn.request("POST", TRADER_REQUEST_PATH, params, headers)

            # Print response data to console
            response = conn.getresponse()
            response = response.read()
            
            # É fundamental utilizar a classe OrderedDict para preservar a ordem dos elementos
            response_json = json.loads(response, object_pairs_hook=OrderedDict)
            
            #print ("status: %s" % response_json['status_code'])
            if('success' in response_json and response_json['success']==0):
                raise ValueError(response_json['message'])
            #print(json.dumps(response_json, indent=4))
            if(nomeRetorno and nomeRetorno!=''):
                return json.dumps(response_json[nomeRetorno], indent=4)
            else:
                return json.dumps(response_json, indent=4)
        finally:
            if conn:
                conn.close()


    def balance(self):
        '''Returns all of your available balances.'''
        params = {}
        return self.__post('balance', params, 'balance')
    
    def complete_balance(self):
        '''Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.'''
        params = {}
        return self.__post('balance', params, 'balance')
    
    def open_orders(self, market):
        '''Returns your open orders for a given market'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')
        
        params = {
                'market': market.value
        }
        return self.__post('open_orders', params, 'order_open')
    
    def trade_history(self, market):
        '''Returns your trade history for a given market'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')
        
        params = {
                'market': market.value
        }
        return self.__post('trade_history', params, 'trade_history')
    
    def deposit_address(self, currency):
        '''Used to get a deposit address by "market".'''
        if(currency and currency!='' and type(currency)!=Currency):
            raise ValueError('Parâmetro currency inválido, utilize a classe Currency.')
        
        params = {
                'currency': currency.value
        }
        return self.__post('deposit_address', params)
    
    def sell(self, market, amount, price):
        '''Places a sell order in a given market.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')
        
        params = {
                'market': market.value,
                'amount': amount,
                'price': price
        }
        return self.__post('sell', params)
    
    def buy(self, market, amount, price):
        '''Places a buy order in a given market.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')
        
        params = {
                'market': market.value,
                'amount': amount,
                'price': price
        }
        return self.__post('buy', params)
    
    def cancel_order(self, market, order_number):
        '''Cancels an order you have placed in a given market.'''
        if(market and market!='' and type(market)!=Market):
            raise ValueError('Parâmetro market inválido, utilize a classe Market.')
        
        params = {
                'market': market.value,
                'order_number': order_number
        }
        return self.__post('cancel_order', params)
