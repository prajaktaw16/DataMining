# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re




# Let's read our CSV file and rename column text to News_Headline
bbc_text = pd.read_csv('/home/prajaktaw/mysite/bbc-text.csv')
bbc_text = bbc_text.rename(columns={'text': 'News_Headline'}, inplace=False)
bbc_text.head(5)


# DATA CLEANING

def cleaning(bbc_text):
    if len(bbc_text) == 1:
        word_tokens = word_tokenize(bbc_text)
    else:
        # Tokenize : dividing Sentences into words
        bbc_text['text_clean'] = bbc_text['News_Headline'].apply(nltk.word_tokenize)
    # Remove stop words
    if len(bbc_text) == 1:
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
    else:
        stop_words = set(nltk.corpus.stopwords.words("english"))
        bbc_text['text_clean'] = bbc_text['text_clean'].apply(lambda x: [item for item in x if item not in stop_words])
    # Will keep words and remove numbers and special characters
    if len(bbc_text) != 1:
        regex = '[a-z]+'
        bbc_text['text_clean'] = bbc_text['text_clean'].apply(lambda x: [char for char in x if re.match(regex, char)])


def detokenize(data):
    for i in range(len(data)):
        bbc_text_w = data['text_clean'][i]
        a = TreebankWordDetokenizer().detokenize(bbc_text_w)
        bbc_text.at[i, 'text_clean'] = a


# Let's assigne numerical values to the unique categories
bbc_text.category = bbc_text.category.map({'tech': 0, 'business': 1, 'sport': 2, 'entertainment': 3, 'politics': 4})
bbc_text.category.unique()

# Check for all the null values if any
bbc_text.isnull().sum()

# Let's split data into train and test
cleaning(bbc_text)
detokenize(bbc_text)
X = bbc_text.text_clean
y = bbc_text.category
# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6, random_state=1)

vector = CountVectorizer(stop_words='english', lowercase=False)
# fit the vectorizer on the training data
vector.fit(X_train)
# print(len(vector.get_feature_names()))
vector.vocabulary_
X_transformed = vector.transform(X_train)
# print(X_transformed.toarray())
X_transformed.toarray()
# for test data
X_test_transformed = vector.transform(X_test)
logistic_reg = LogisticRegression()
logistic_reg.fit(X_transformed, y_train)

# fit
logistic_reg.fit(X_transformed, y_train)

# predict class
y_predicted = logistic_reg.predict(X_test_transformed)

# predict probabilities
y_pred_probability = logistic_reg.predict_proba(X_test_transformed)

# printing the overall accuracy
metrics.accuracy_score(y_test, y_predicted)

confusion_mat = metrics.confusion_matrix(y_test, y_predicted)
TrueNeg = confusion_mat[0, 0]
TruePos = confusion_mat[1, 1]
FalseNeg = confusion_mat[1, 0]
FalsePos = confusion_mat[0, 1]
sensitivity = TruePos / float(FalseNeg + TruePos)
specificity = TrueNeg / float(TrueNeg + FalsePos)

PRECISION_SCORE = metrics.precision_score(y_test, y_predicted, average='micro')
RECALL_SCORE = metrics.recall_score(y_test, y_predicted, average='micro')
F1_SCORE = metrics.f1_score(y_test, y_predicted, average='micro')

naivebayes = MultinomialNB()
naivebayes.fit(X_transformed, y_train)

# fit
naivebayes.fit(X_transformed, y_train)
# predict class
y_predict = naivebayes.predict(X_test_transformed)
# predict probabilities
y_pred_probability = naivebayes.predict_proba(X_test_transformed)

# printing the overall accuracy
metrics.accuracy_score(y_test, y_predict)

# confusion matrix
metrics.confusion_matrix(y_test, y_predict)
# help(metrics.confusion_matrix)

confusion = metrics.confusion_matrix(y_test, y_predict)

TrueNeg = confusion_mat[0, 0]
TruePos = confusion_mat[1, 1]
FalseNeg = confusion_mat[1, 0]
FalsePos = confusion_mat[0, 1]
sensitivity = TruePos / float(FalseNeg + TruePos)

specificity = TrueNeg / float(TrueNeg + FalsePos)

PRECISION_SCORE = metrics.precision_score(y_test, y_predicted, average='micro')
RECALL_SCORE = metrics.recall_score(y_test, y_predicted, average='micro')
F1_SCORE = metrics.f1_score(y_test, y_predicted, average='micro')


def predict_class(headline):
    list1=[]
    list1.append(headline)
    vec4 = vector.transform(list1).toarray()
    classify = (str(list(naivebayes.predict(vec4))[0]).replace('0', 'TECH').replace('1', 'BUSINESS').replace('2',
                                                                                                             'SPORTS').replace(
        '3', 'ENTERTAINMENT').replace('4', 'POLITICS'))
    return classify


