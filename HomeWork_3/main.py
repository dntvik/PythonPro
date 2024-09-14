import csv
from io import StringIO
import requests
from flask import Flask, jsonify, make_response
from faker import Faker
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)
fake = Faker()


def generate_students_data(count):
    students = []

    for _ in range(count):
        student = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "birthday": fake.date_of_birth(minimum_age=18, maximum_age=60).strftime(
                "%Y-%m-%d"
            ),
        }
        students.append(student)
    return students


students_args = {
    "count": fields.Int(load_default=100, validate=lambda val: 1 <= val <= 1000)
}


@app.route("/generate_students")
@use_args(students_args, location="query")
def generate_students(args):
    count = args["count"]
    students = generate_students_data(count)
    return jsonify(students)


@app.route("/generate_students/download_csv")
@use_args(students_args, location="query")
def download_csv(args):
    count = args["count"]
    students = generate_students_data(count)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["First Name", "Last Name", "Email", "Password", "Birthday"])

    for student in students:
        writer.writerow(
            [
                student["first_name"],
                student["last_name"],
                student["email"],
                student["password"],
                student["birthday"],
            ]
        )

    csv_content = output.getvalue()

    response = make_response(csv_content)
    response.headers["Content-Disposition"] = "attachment; filename=students.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


bitcoin_rate_args = {
    "currency": fields.Str(load_default="USD"),
    "count": fields.Int(load_default=1),
}

currency_symbols = {}


def fetch_currency_symbol(currency_code):
    url = "https://test.bitpay.com/currencies"
    response = requests.get(url)
    data = response.json()
    currency_symbols = {
        currency["code"]: currency["symbol"] for currency in data["data"]
    }
    return currency_symbols.get(currency_code.upper(), currency_code)


def get_bitcoin_value(currency="USD", count=1):
    api_url = f"https://bitpay.com/api/rates/{currency}"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch Bitcoin value: {response.status_code} {response.reason}"
        )
    data = response.json()
    bitcoin_rate = data["rate"]
    converted_value = bitcoin_rate * count
    return f"{converted_value}"


@app.route("/bitcoin_rate")
@use_args(bitcoin_rate_args, location="query")
def bitcoin_rate(args):
    currency_code = args["currency"].upper()
    currency = fetch_currency_symbol(currency_code)
    count = args["count"]
    value = get_bitcoin_value(currency_code, count)
    return f"{value} {currency_code} ({currency}) to buy {count} BTC"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
