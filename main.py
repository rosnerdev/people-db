import sqlite3
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def add_person(name, age):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS people
                 (name text, age integer)''')

    c.execute(f'INSERT INTO people (name, age) VALUES ("{name}", "{age}")')

    conn.commit()
    conn.close()

    print(f'Name: {name}, Age: {age} were submitted successfully!')

@app.route('/')
def index():
    conn = sqlite3.connect('people.db', detect_types=sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS people
                 (name text, age integer)''')

    c.execute("SELECT * FROM people")

    rows = c.fetchall()

    people_list = []

    for row in rows:
        people_list.append({'name': row[0], 'age': row[1]})

    conn.close()

    return render_template('index.html', list=people_list)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    args = request.args

    name = args['name']
    age = args['age']

    add_person(name, age)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
