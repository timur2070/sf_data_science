import requests
import json
from config import API_KEY, KEYS

class ConversionError(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):

        if base == quote:
            raise ConversionError('The base and the quote currency are the same.')
        try:
            base_ticker = KEYS[base]
        except KeyError:
            raise ConversionError(f'No such currency in database: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionError('Check the spelling for the amount. The correct format is 0.00')

        try:
            quote_ticker = KEYS[quote]
        except KeyError:
            raise ConversionError(f'No such currency in database: {quote}')

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}0&apikey={API_KEY}')
        result = json.loads(r.content)['result']
        return result



