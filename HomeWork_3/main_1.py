import csv
from io import StringIO
from flask import Flask, request, jsonify, make_response
from faker import Faker

app = Flask(__name__)
fake = Faker()


def generate_students_data(count):
    students = []
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Password', 'Birthday'])

    for _ in range(count):
        student = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': fake.password(),
            'birthday': fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
        }
        students.append(student)
        writer.writerow(
            [student['first_name'], student['last_name'],
            student['email'], student['password'],
            student['birthday']])

    csv_content = output.getvalue()
    return students, csv_content


@app.route('/generate_students')
def generate_students():
    count = int(request.args.get('count', 100))

    if count > 1000:
        return jsonify({"error": "Limit is 1000 students."}), 400

    students, _ = generate_students_data(count)

    return jsonify(students)


@app.route('/generate_students/download_csv')
def download_csv():
    count = int(request.args.get('count', 100))

    if count > 1000:
        return jsonify({"error": "Limit is 1000 students."}), 400

    _, csv_content = generate_students_data(count)

    response = make_response(csv_content)
    response.headers['Content-Disposition'] = 'attachment; filename=students.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
