'''

Link do Dataset usado: https://www.kaggle.com/code/frankschindler1/sentiment-analysis-tripadvisor-reviews

'''

#Importando bibliotenas
import string
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import pickle
from wordcloud import WordCloud

# Pré-processamento e avaliação
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.regularizers import l1, l2

# Modelos
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB

import nltk
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('rslp')
nltk.download('averaged_perceptron_tagger')
nltk.download('mac_morpho')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download("maxent_ne_chunker")
nltk.download("words")


# Importando dataser
df = pd.read_csv('D:/Programação/ProjetoIntegrador4-Backend/Backend/Endpoint/tripadvisor_hotel_reviews.csv')

df = df[:2000]

df.head()

#Mostrando infos de dataset
df.info()


#===============================================================================================================

#Visualizando os dados
sns.countplot(data=df, x='Rating', palette='flare').set_title('Rating Distribution Across Dataset')

# Comprimento da palavra na frase
df['Length'] = df['Review'].apply(len)
df.head()

sns.displot(data=df, x='Length', hue='Rating', palette='flare', kind='kde', fill=True, aspect=4)

g = sns.FacetGrid(data=df, col='Rating')
g.map(plt.hist, 'Length', color='#973aa8')

sns.stripplot(data=df, x='Rating', y='Length', palette='flare', alpha=0.3)


#===============================================================================================================

#  Alterar a classificação para ser mais simples e mais fácil de entender

def rating(score):
    print(score)
    if score > 3:
        return 'Good'
    elif score == 3:
        return 'Netral'
    else:
        return 'Bad'

df['Rating'] = df['Rating'].apply(rating)

df.head()

# Total de palavras no conjunto de dados antes da limpeza
length = df['Length'].sum()

print('Original:')
print(df['Review'][0])
print()

sentence = []
for word in df['Review'][0].split():
    stemmer = SnowballStemmer('english')
    sentence.append(stemmer.stem(word))
print('Stemming:')
print(' '.join(sentence))
print()

sentence = []
for word in df['Review'][0].split():
    lemmatizer = WordNetLemmatizer()
    sentence.append(lemmatizer.lemmatize(word, 'v'))
print('Lemmatization:')
print(' '.join(sentence))

def cleaning(text):
    #remover pontuações e letras maiúsculas
    clean_text = text.translate(str.maketrans('','',string.punctuation)).lower()
    
   #remover palavras irrelevantes
    clean_text = [word for word in clean_text.split() if word not in stopwords.words('english')]
    
    #lematizar a palavra
    sentence = []
    for word in clean_text:
        lemmatizer = WordNetLemmatizer()
        sentence.append(lemmatizer.lemmatize(word, 'v'))

    return ' '.join(sentence)

df['Review'] = df['Review'].apply(cleaning)


df['Length'] = df['Review'].apply(len)
new_length = df['Length'].sum()

print('Comprimento total do texto antes da limpeza: {}'.format(length))
print('Comprimento total do depois antes da limpeza: {}'.format(new_length))

df.to_csv('cleaned_df.csv', index=False)


#===============================================================================================================


# Após a limpeza, encontrar a palavra mais usada
plt.figure(figsize=(20,20))
wc = WordCloud(max_words=1000, min_font_size=10, 
                height=800,width=1600,background_color="white", colormap='flare').generate(' '.join(df['Review']))

plt.imshow(wc)

X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Rating'], test_size=0.2)

#===============================================================================================================


tfid = TfidfVectorizer()
train_tfid_matrix = tfid.fit_transform(X_train)
test_tfid_matrix = tfid.transform(X_test)

pickle.dump(tfid, open('tfidf.pkl', 'wb'))

models = [DecisionTreeClassifier(),
          RandomForestClassifier(),
          SVC(),
          LogisticRegression(max_iter=1000),
          KNeighborsClassifier(),
          BernoulliNB()]

accuracy = []

for model in models:
    cross_val = cross_val_score(model, train_tfid_matrix, y_train, scoring='accuracy',
                               cv=StratifiedKFold(10)).mean()
    accuracy.append(cross_val)

models_name = ['DecisionTreeClassifier', 'RandomForestClassifier', 'SVC',
         'LogisticRegression', 'KNeighborsClassifier', 'BernoulliNB']

acc = pd.DataFrame({'Model': models_name, 'Accuracy': accuracy})
acc

log = LogisticRegression(max_iter=1000)
log.fit(train_tfid_matrix, y_train)

pred = log.predict(test_tfid_matrix)

pickle.dump(log, open('ml_model.pkl', 'wb'))

ml = pickle.load(open('ml_model.pkl','rb'))
tfidf = pickle.load(open('tfidf.pkl','rb'))

def ml_predict(text):
    clean_text = cleaning(text)
    tfid_matrix = tfidf.transform([clean_text])
    pred_proba = ml.predict_proba(tfid_matrix)
    idx = np.argmax(pred_proba)
    pred = ml.classes_[idx]
    
    return pred, pred_proba[0][idx]

ml_predict('poor room service')

print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

tokenizer = Tokenizer(num_words=50000, oov_token='<OOV>')

tokenizer.fit_on_texts(X_train)
# print(tokenizer.word_index)
total_word = len(tokenizer.word_index)+1
print('Total distinct words: {}'.format(total_word))

train_seq = tokenizer.texts_to_sequences(X_train)
train_padded = pad_sequences(train_seq)

test_seq = tokenizer.texts_to_sequences(X_test)
test_padded = pad_sequences(test_seq)

lb = LabelBinarizer()
train_labels = lb.fit_transform(y_train)
test_labels = lb.transform(y_test)

pickle.dump(tokenizer, open('tokenizer.pkl', 'wb'))
pickle.dump(lb, open('label.pkl', 'wb'))

model = tf.keras.models.Sequential([tf.keras.layers.Embedding(total_word, 8),
                                    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Dense(8, kernel_regularizer=l2(0.001),
                                                          bias_regularizer=l2(0.001), activation='relu'),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Dense(3, activation='softmax')])

model.summary()

model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_padded, train_labels, epochs=25, validation_data=(test_padded, test_labels))

metrics = pd.DataFrame(model.history.history)
metrics[['accuracy', 'val_accuracy']].plot()
metrics[['loss', 'val_loss']].plot()

pred2 = model.predict(test_padded)

true_labels = np.argmax(test_labels, axis=-1)
pred_labels = np.argmax(pred2, axis=-1)

print(confusion_matrix(true_labels, pred_labels))
print(classification_report(true_labels, pred_labels))

model.save('dl_model.h5')

# Regressão Logística
def ml_predict(text):
    clean_text = cleaning(text)
    tfid_matrix = tfid.transform([clean_text])
    pred = log.predict(tfid_matrix)[0]
    
    return pred

# Rede Neural
def dl_predict(text):
    clean_text = cleaning(text)
    seq = tokenizer.texts_to_sequences([clean_text])
    padded = pad_sequences(seq)

    pred = model.predict(padded)
    # Recuperar o nome do rótulo
    result = lb.inverse_transform(pred)[0]
    
    return result

