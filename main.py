from flask import Flask, render_template, request  # Import Flask modules
from transformers import pipeline  # Import pipeline from transformers
import sqlite3  # Import sqlite3

app = Flask(__name__)


# Initialize database
def init_db():
    with sqlite3.connect(r"C:\Users\esvit\Data Science\Machine Learning\Py\Ang\backend dev with flask\sentiment-analysis web app\sentiment.db") as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sentiment_table
                        (
                            
                        user_text TEXT NOT NULL,
                        sentiment TEXT  NOT NULL,
                        score FLOAT not null
                        );'''
                       )
        db.commit()

init_db() 



# Load the sentiment analysis model once during startup to avoid reloading
pipe = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

@app.route('/', methods=['GET', 'POST'])
def check_sentiment():
    result = None  # Default result before user submits
    if request.method == 'POST':
        text = request.form['text']
        result = pipe(text)  # Perform sentiment analysis


        label = result[0]['label']
        score = result[0]['score']

        #store the result in the database
        with sqlite3.connect(r"C:\Users\esvit\Data Science\Machine Learning\Py\Ang\backend dev with flask\sentiment-analysis web app\sentiment.db") as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO sentiment_table(user_text, sentiment, score) VALUES(?, ?, ?)''', 
                           (text, label, score))
            db.commit()

          

    
    return render_template('index.html', result=result)  # Pass result to template

if __name__ == '__main__':
    app.run(debug=True)
