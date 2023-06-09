from flask import Flask,render_template,request
import pickle
import numpy as np

#popular_df = pickle.load(open('popular.pkl','rb'))
# pt = pickle.load(open('pt.pkl','rb'))
popular_df = pickle.load(open('courses.pkl','rb'))
similarity_scores = pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           course_name = list(popular_df['course_name'].values),
                           course_univ=list(popular_df['University'].values),
                           course_difficulty=list(popular_df['difficulty_level'].values),
                           course_rating=list(popular_df['course_rating'].values),

                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = popular_df[popular_df['course_name'] == user_input].index[0]
    distances = sorted(list(enumerate(similarity_scores[index])), reverse=True, key=lambda x: x[1])
    data = []
    for i in distances[1:7]:
        item=[]
        item.append(popular_df.iloc[i[0]].course_name)
        item.append(popular_df.iloc[i[0]].University)
        item.append(popular_df.iloc[i[0]].difficulty_level)
        item.append(popular_df.iloc[i[0]].course_rating)
        data.append(item)

       


#     #index = np.where(pt.index == user_input)[0][0]
#     #similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

#     # data = []
#     # for i in similar_items:
#     #     item = []
#     #     temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

#     #     data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)