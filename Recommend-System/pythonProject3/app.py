import inline
import matplotlib
import nltk
from django.contrib.sites import requests
from flask import Flask,render_template,request
import pickle
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
nltk.download("stopwords")

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df=pickle.load(open('data.pkl','rb'))
df_new=pickle.load(open('data1.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(df_new['book_title'].values),
                           author=list(df_new['book_author'].values),
                           image=list(df_new['im_url'].values),
                           pages=list(df_new['numpages'].values),
                           rating=list(df_new['averageRating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input in df['book_title'].values:
        rating_counts = df['rating_count'][df['rating_count'] <= 100].index
        rare_books = rating_counts <= 100
        common_books = df[~df['book_title'].isin(rare_books)]

        if user_input in rare_books:
            books = []
            common_books = common_books.drop_duplicates(subset=['book_title'])
            common_books.reset_index(inplace=True)
            common_books['index'] = [i for i in range(common_books.shape[0])]
            random = common_books['index'].unique().sample(5).values
            for i in random:
                item = []
                temp_df = common_books[common_books['index'] == i[0]]
                item.extend(list(temp_df.drop_duplicates('book_title')['book_title'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['book_author'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['im_url'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['numpages'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['averageRating'].values))
                books.append(item)

            print(books)

        else:

            common_books = common_books.drop_duplicates(subset=['book_title'])
            common_books.reset_index(inplace=True)
            common_books['index'] = [i for i in range(common_books.shape[0])]
            target_cols = ['book_title', 'book_author', 'publisher', 'category', 'book_length']
            common_books['combined_features'] = [' '.join(common_books[target_cols].iloc[i,].values) for i in
                                                 range(common_books[target_cols].shape[0])]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(count_matrix)
            index = common_books[common_books['book_title'] == user_input]['index'].values[0]
            sim_books = list(enumerate(cosine_sim[index]))
            sorted_sim_books = sorted(sim_books, key=lambda x: x[1],
                                      reverse=True)[1:6]

            books = []
            for i in sorted_sim_books:
                item = []
                temp_df = common_books[common_books['index'] == i[0]]
                item.extend(list(temp_df.drop_duplicates('book_title')['book_title'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['book_author'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['im_url'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['numpages'].values))
                item.extend(list(temp_df.drop_duplicates('book_title')['averageRating'].values))
                books.append(item)

            print(books)


    return render_template('recommend.html',data=books)
if __name__ == '__main__' :
    app.run(debug=True)