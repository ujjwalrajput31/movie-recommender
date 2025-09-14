from flask import Flask, render_template, request
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load your saved data/model (update paths if needed)
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

def recommend(movie):
    """Return list of recommended movies based on similarity index"""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Get top 5 similar movies
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommendations = []
    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)
    return recommendations

@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend_movie():
    user_input = request.form.get('movie')
    recommendations = recommend(user_input)
    return render_template('recommend.html', movie=user_input, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
