import os
from flask import Flask, render_template, request
from transformers import pipeline
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database URL from Render.com environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")  # Render sets this
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define model
class SentimentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Load model
pipe = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

@app.route('/', methods=['GET', 'POST'])
def check_sentiment():
    result = None
    if request.method == 'POST':
        text = request.form['text']
        result = pipe(text)

        label = result[0]['label']
        score = result[0]['score']

        # Save to DB
        new_entry = SentimentResult(user_text=text, sentiment=label, score=score)
        db.session.add(new_entry)
        db.session.commit()

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
