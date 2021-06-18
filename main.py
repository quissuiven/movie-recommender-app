app = Flask(__name__)

# SqlAlchemy Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./users4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #set to False to reduce overhead
db = SQLAlchemy(app)

#Define SQLAlchemy ORM User model
class User(db.Model):
    __tablename__ = 'users4'
    user_id = db.Column(Integer, primary_key=True, index=True)
    name = db.Column(String(50), nullable=True)
    movie_type = Column(String)
    genres = Column(String)
    nationality = Column(String)
    email = Column(String, nullable=True)

    def __init__(self, name, movie_type, genres, nationality, email):
        self.name = name
        self.movie_type = movie_type
        self.genres = genres
        self.nationality = nationality
        self.email = email

#Create tables and database
db.create_all()

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/', methods = ['POST'])
def create_users():
    if request.method == 'POST':
        #get user info when user submits form
        name = request.form.get('name')
        user_movie_type = request.form.getlist('movie_type')
        user_genre = request.form.getlist('genre')
        user_nationality = request.form.getlist('nationality')
        email = request.form.get('email')

        #add user to database
        user = User(name, json.dumps(user_movie_type), json.dumps(user_genre), json.dumps(user_nationality), email)
        db.session.add(user)
        db.session.commit()

        #connect to movie database to identify movies catered to user choice
        movie_db = sql.connect('movie_recsys4.db')
        movie_df = pd.read_sql("SELECT title_id, title, region, movie_type, genres_list, image, averageRating from movie where image != 'nan' and overview != 'nan' and actor_name != 'nan' and director_name != 'nan'", movie_db)
        movie_df = movie_df.loc[movie_df.movie_type.isin(user_movie_type) & movie_df.region.isin(user_nationality)]
        movie_df['genres_list'] = movie_df['genres_list'].apply(lambda x: json.loads(x))

        def has_overlapping_genres(row):
            return bool(set(user_genre) & set(row.genres_list))

        movie_df['has_overlapping_genres'] = movie_df.apply(has_overlapping_genres, axis = 1)
        result = movie_df.query('has_overlapping_genres == True').sort_values(by = 'averageRating', ascending = False).iloc[0:10]
        result_json = result.to_json(orient="split")

        #pass recommended movies to get_movies function
        return redirect(url_for('get_movies', messages = result_json))

@app.route('/movies', methods = ['GET'])
def get_movies():
    if request.method == 'GET':
        #gets recommended movies and display info such as title, image, genres and rating in html
        messages = request.args['messages']
        top_movies_df = pd.read_json(messages, orient='split')
        movie1_titleid = top_movies_df['title_id'].iloc[0]
        movie1_title = top_movies_df['title'].iloc[0]
        movie1_genres = ', '.join(top_movies_df['genres_list'].iloc[0])
        movie1_image = top_movies_df['image'].iloc[0]
        movie1_averageRating = top_movies_df['averageRating'].iloc[0]
        movie2_titleid = top_movies_df['title_id'].iloc[1]
        movie2_title = top_movies_df['title'].iloc[1]
        movie2_genres = ', '.join(top_movies_df['genres_list'].iloc[1])
        movie2_image = top_movies_df['image'].iloc[1]
        movie2_averageRating = top_movies_df['averageRating'].iloc[1]
        movie3_titleid = top_movies_df['title_id'].iloc[2]
        movie3_title = top_movies_df['title'].iloc[2]
        movie3_genres = ', '.join(top_movies_df['genres_list'].iloc[2])
        movie3_image = top_movies_df['image'].iloc[2]
        movie3_averageRating = top_movies_df['averageRating'].iloc[2]
        return render_template("movies.html", movie1_titleid = movie1_titleid, movie1_title = movie1_title, movie1_genres = movie1_genres, movie1_image = movie1_image, movie1_averageRating = movie1_averageRating, \
                                              movie2_titleid = movie2_titleid, movie2_title = movie2_title, movie2_genres = movie2_genres, movie2_image = movie2_image, movie2_averageRating = movie2_averageRating, \
                                              movie3_titleid = movie3_titleid, movie3_title = movie3_title, movie3_genres = movie3_genres, movie3_image = movie3_image, movie3_averageRating = movie3_averageRating)

@app.route('/selected_movie', methods = ['POST'])
def show_movie():
    if request.method == 'POST':
        #get movieid of movie that user clicked
        selected_movieid = request.form.get('selected_movieid')

        #for given movieid, extract info from movie database
        movie_db = sql.connect('movie_recsys4.db')
        selected_movie = pd.read_sql("SELECT title, region, movie_type, genres_list, actor_name, director_name, averageRating, overview, image, top_movies FROM movie WHERE title_id = ? and image != 'nan' and overview != 'nan' and actor_name != 'nan' and director_name != 'nan'", movie_db, params = (selected_movieid,))
        movie_title = selected_movie['title'][0]
        movie_region = selected_movie['region'][0]
        movie_movietype = selected_movie['movie_type'][0]
        movie_genres = ', '.join(selected_movie['genres_list'].apply(lambda x: json.loads(x))[0])
        movie_actor_name = ', '.join(selected_movie['actor_name'].apply(lambda x: json.loads(x))[0])
        movie_director_name = selected_movie['director_name'][0]
        movie_averageRating = selected_movie['averageRating'][0]
        movie_overview = selected_movie['overview'][0]
        movie_image = selected_movie['image'][0]

        #Get top similar movies and display info in html
        first_rec_title_id = json.loads(selected_movie['top_movies'][0])[0][0]
        first_rec_title = json.loads(selected_movie['top_movies'][0])[0][1]
        first_rec_image = json.loads(selected_movie['top_movies'][0])[0][2]
        second_rec_title_id = json.loads(selected_movie['top_movies'][0])[1][0]
        second_rec_title = json.loads(selected_movie['top_movies'][0])[1][1]
        second_rec_image = json.loads(selected_movie['top_movies'][0])[1][2]
        third_rec_title_id = json.loads(selected_movie['top_movies'][0])[2][0]
        third_rec_title = json.loads(selected_movie['top_movies'][0])[2][1]
        third_rec_image = json.loads(selected_movie['top_movies'][0])[2][2]
        fourth_rec_title_id = json.loads(selected_movie['top_movies'][0])[3][0]
        fourth_rec_title = json.loads(selected_movie['top_movies'][0])[3][1]
        fourth_rec_image = json.loads(selected_movie['top_movies'][0])[3][2]
        fifth_rec_title_id = json.loads(selected_movie['top_movies'][0])[4][0]
        fifth_rec_title = json.loads(selected_movie['top_movies'][0])[4][1]
        fifth_rec_image = json.loads(selected_movie['top_movies'][0])[4][2]
        return render_template("selected_movie.html", movie_title = movie_title, movie_region = movie_region, movie_movietype = movie_movietype, movie_genres = movie_genres, movie_actor_name = movie_actor_name, movie_director_name = movie_director_name, movie_averageRating = movie_averageRating, movie_overview = movie_overview, movie_image = movie_image, \
                               first_rec_title_id = first_rec_title_id, first_rec_title = first_rec_title, first_rec_image = first_rec_image,
                               second_rec_title_id = second_rec_title_id, second_rec_title = second_rec_title, second_rec_image = second_rec_image,
                               third_rec_title_id = third_rec_title_id, third_rec_title = third_rec_title, third_rec_image = third_rec_image,
                               fourth_rec_title_id = fourth_rec_title_id, fourth_rec_title = fourth_rec_title, fourth_rec_image = fourth_rec_image,
                               fifth_rec_title_id = fifth_rec_title_id, fifth_rec_title = fifth_rec_title, fifth_rec_image = fifth_rec_image)

if __name__ == '__main__':
    app.run()
