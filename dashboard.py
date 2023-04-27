from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# mock data for students and quizzes
students = [
    {'id': 1, 'first_name': 'John', 'last_name': 'Doe'},
    {'id': 2, 'first_name': 'Jane', 'last_name': 'Doe'},
    {'id': 3, 'first_name': 'Bob', 'last_name': 'Smith'},
]

quizzes = [
    {'id': 1, 'subject': 'Math', 'num_questions': 10, 'quiz_date': '2022-05-01'},
    {'id': 2, 'subject': 'Science', 'num_questions': 15, 'quiz_date': '2022-05-03'},
    {'id': 3, 'subject': 'History', 'num_questions': 20, 'quiz_date': '2022-05-05'},
]

@app.route('/dashboard')
def dashboard():
    # pass the student and quiz data to the dashboard template
    return render_template('dashboard.html', students=students, quizzes=quizzes)

if __name__ == '__main__':
    app.run()