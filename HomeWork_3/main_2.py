import requests
from flask import Flask, request

app = Flask(__name__)

currency_symbols = {}


def fetch_currency_symbols():
    global currency_symbols
    url = "https://test.bitpay.com/currencies"
    response = requests.get(url)
    data = response.json()
    currency_symbols = {currency["code"]: currency["symbol"] for currency in data['data']}
    return currency_symbols


fetch_currency_symbols()


def get_currency_symbol(currency):
    return currency_symbols.get(currency.upper(), currency)


def get_bitcoin_value(currency="USD", count=1):
    api_url = f"https://bitpay.com/api/rates/{currency}"
    response = requests.get(api_url)
    data = response.json()
    bitcoin_rate = data['rate']
    converted_value = bitcoin_rate * count
    return f"{converted_value}"


@app.route('/bitcoin_rate')
def bitcoin_rate():
    currency_code = request.args.get('currency', 'USD').upper()
    currency = get_currency_symbol(currency_code)
    count = int(request.args.get('count', 1))
    value = get_bitcoin_value(currency_code, count)
    return f'{value} {currency_code} ({currency}) to buy {count} BTS'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
