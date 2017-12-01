from flask import Flask, url_for
from flask import render_template
from flask import request
from textblob import TextBlob
import pandas as pd
app = Flask(__name__)

@app.route('/')
def home():
    #review_file = open( url_for('static', filename='restaurant-data.txt'), 'r')
    review_file = open( 'static/restaurant-data.txt', 'r')
    reviews = review_file.readline()
    reviews = reviews.split('"')
    reviews = set(reviews)
    # we store the data here
    results = []
    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        status = 'Negative'
        if polarity >= 0: status = 'Positive'
        results.append({
            'review': review,
            'polarity': polarity,
            'status': status
        })
    results_df = pd.DataFrame(results)
    positives = results_df[results_df['status'].str.contains('Positive')]
    negatives = results_df[~results_df['status'].str.contains('Positive')]
    print results_df.head(10)
    return render_template('index.html', results_list = results, pos = positives, neg = negatives)

@app.route('/analyze')
def analyze():
    txtBlob = request.args.get('txtBlob')
    txtBlob = TextBlob(txtBlob)
    print txtBlob.sentiment
    return render_template('sentiment.html', text=txtBlob, polarity=txtBlob.sentiment.polarity)

if __name__=='__main__':
    app.debug = True
    app.run()
