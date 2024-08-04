from random import randint, choices
import string
import pandas as pd
from flask import Flask

app = Flask(__name__)


@app.route("/generate-password")
def generate_password():
    password_length = (
        randint(10, 20))

    return "".join(
        choices(
            string.digits + string.ascii_letters +
            string.punctuation, k=password_length))


@app.route("/calculate_average")
def calculate_average():
    file_path = "hw.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    average_height = df['Height(Inches)'].mean()
    average_weight = df['Weight(Pounds)'].mean()
    return f'Average weight = {average_weight}, Average height = {average_height}'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
