from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import nltk

# Auto-download required corpus
nltk.download('punkt', quiet=True)

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend is running 👍"

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()

    def get_sentiment(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return 'Positive'
        elif polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    if 'texts' in data:
        results = [{'text': text, 'sentiment': get_sentiment(text)} for text in data['texts']]
        return jsonify({'results': results})
    elif 'text' in data:
        sentiment = get_sentiment(data['text'])
        return jsonify({'sentiment': sentiment})
    else:
        return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run()
