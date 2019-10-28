# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:53:45 2019

@author: Sriram Sivaraman
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:09:45 2019

@author: Kapil.Gurjar

Modification History:
    - [2019-10-11] (Vishal Bala) -- Maintain separate vectorizers/transformers for classification vs. sentiment
    - [2019-10-11] (Vishal Bala) -- Fixed a bug where predictions were being returned as arrays instead of integers
    - [2019-10-11] (Vishal Bala) -- General formatting clean-up + documentation
    - [2019-10-11] (Vishal Bala) -- Added integrated Flask request parsing/validation + error handling
    - [2019-10-11] (Vishal Bala) -- Updated API to use actual status codes instead of embedding status in response data
"""

# ===============
#    LIBRARIES
# ===============

import joblib
import nltk
import numpy as np
from flask import Flask
from flask_restful import Api, reqparse, Resource

import config_fasttext as cfg
from text_preparation_fast_text import TextPreparer,TextPreparerSentiment
import fasttext

# =======================
#    GLOBAL PARAMETERS
# =======================

# Words shorter than this number of characters are excluded from ML operations
MIN_WORD_LENGTH = 2

# A map of supported language codes to the full language names that can be supplied
# NOTE: Both values will be accepted by the API, and will be processed as the dictionary values in practice
LANGUAGES = {
    'eng': 'english',
}


# ===================
#    MODEL LOADING
# ===================

nltk.download('stopwords')
CV_loaded_c = joblib.load(cfg.count_vect_c)
tfidf_loaded_c = joblib.load(cfg.tfidf_transformer_c)
sentiment_loaded = fasttext.load_model(cfg.sentiment_model)

loaded_model = {}
for [key, val] in cfg.category_models.items():
    loaded_model[key] = joblib.load(val)


# =====================
#    REQUEST PARSING
# =====================

parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument(
    'message',
    type=str,
    required=True,
    help='Must provide a text review to evaluate.'
)

parser.add_argument(
    'language',
    choices=set(LANGUAGES.keys()) | set(LANGUAGES.values()),
    required=True,
    help='Invalid language: {error_msg}'
)

parser.add_argument(
    'integration_type',
    type=str,
    required=False,
    help='Must be the channel through which the review was acquired.'
)


# ========================
#    CLASSIFICATION API
# ========================

class Classify(Resource):
    """An endpoint for classifying review data into content categories, and analyzing text sentiment."""

    def post(self):
        """
        Fields:
            message:            The body of the review.
            language:           The language (code) which the review is in.
            integration_type:   The channel through which the review was acquired.
        """
        status_code = 200

        # Extract and validate the data of the request
        posted_data = parser.parse_args()

        # Extract the body of the review
        message = posted_data['message']

        # Extract the language of the review
        language = posted_data['language']
        if language in LANGUAGES:  # Handle cases where a language "code" was supplied to the API
            language = LANGUAGES[language]

        # Extract the channel through which the review was acquired
        integration_type = posted_data['integration_type']

        reviews = np.array([message])

        # Identify categories associated with the review
        tp = TextPreparer(reviews, integration_type, tfidf_loaded_c, CV_loaded_c, language, MIN_WORD_LENGTH)
        X_bow = tp.bag_of_words_string()
        categories = []
        for key, val in loaded_model.items():
            cat_score = int(val.predict(X_bow)[0])
            if cat_score == 1:
                categories.append(key)

        # Identify the sentiment of the review (positive/neutral/negative)
        tp = TextPreparerSentiment(reviews, integration_type, language, MIN_WORD_LENGTH)
        X_bow = tp.bag_of_words_string()
        sentiment = int(sentiment_loaded.predict(X_bow)[0][0].split('__')[2])  # -1 is negative, 0 is neutral, 1 is positive

        return {
            'categories': categories or None,
            'sentiment': sentiment
        }, status_code


# ===============
#    EXECUTION
# ===============

app = Flask(__name__)
api = Api(app)
api.add_resource(Classify, '/classify')

if __name__ == '__main__':
    # Instantiate the API, configure the classification endpoint, and run it perpetually
    app.run(host='0.0.0.0')
