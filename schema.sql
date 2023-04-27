CREATE TABLE Students (
    ID INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE Quizzes (
    ID INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    date_given DATE NOT NULL
);

CREATE TABLE Results (
    student_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    PRIMARY KEY (student_id, quiz_id),
    FOREIGN KEY (student_id) REFERENCES Students(ID),
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(ID)
);