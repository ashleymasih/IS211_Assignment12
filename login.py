from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'thekey'


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        error = request.args.get('error')
        return render_template('login.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('hw13.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students")
    students = cur.fetchall()
    cur.execute("SELECT * FROM quizzes")
    quizzes = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/quiz/add', methods= ['GET', 'POST'])
def add_quiz():
    subject = ''
    num_questions = ''
    quiz_date = ''
    error = ''

    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['date_given']

    if not subject or not num_questions or not quiz_date:
        error = 'Please fill in all information'
        return render_template('add_quiz.html', error = error)
    
    try:
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO quizzes (subject, num_questions, date_given) VALUES (?, ?, ?)", 
                        (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    except:
        error = 'Error adding quiz. Please try again.'
        return render_template('add_quiz.html', error=error)
    
@app.route('/student/<id>')
def quiz_results(id):
    try:
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute("SELECT quizzes.id, Results.score FROM quizzes JOIN Results ON quizzes.id = Results.quiz_id JOIN Students ON Results.student_id = Students.ID WHERE Students.ID=?", (id,))
        quiz_results = cur.fetchall()
        if not quiz_results:
            return "No results found for quiz"
        cur.execute("SELECT first_name, last_name FROM students WHERE id=?", (id,))
        student = cur.fetchone()
        conn.close()
        return render_template('quiz_results.html', student=student, quiz_results=quiz_results)
    except:
        return "Error displaying quiz results"
    
@app.route('/results/add', methods=['GET'])
def add_result():
    try:
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()

        # Get all students and quizzes from the database
        cur.execute("SELECT * FROM Students")
        students = cur.fetchall()
        cur.execute("SELECT * FROM Quizzes")
        quizzes = cur.fetchall()

        # Render the add_result.html template with the students and quizzes
        return render_template('add_result.html', students=students, quizzes=quizzes)

    except:
        return "Error displaying add quiz result form"
    
@app.route('/results/add', methods=['POST'])
def submit_result():
    try:
        # Get the form data from the request
        student_id = request.form['student']
        quiz_id = request.form['quiz']
        score = request.form['score']

        # Connect to the database and insert the quiz result
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Results (student_id, quiz_id, score) VALUES (?, ?, ?)", (student_id, quiz_id, score))
        conn.commit()
        conn.close()

        # Redirect to the dashboard
        return redirect(url_for('dashboard'))

    except:
        # If there was an error, redirect back to the add_result route with an error message
        return render_template('add_result.html', error="Error adding quiz result")
    


if __name__ == '__main__':
    app.run()