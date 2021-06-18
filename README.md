# Movie Recommender App

This is a simple web application utilising Content-based filtering algorithm to recommend movies to users. Content-based filtering is used as it can make good recommendations while avoiding the cold-start problem. 

**load_data.ipynb** scrapes movie data from IMDB, does the preprocessing, computes similarity between movies based on several features (movie type, movie genres, actor name, director name, keywords) and stores the movie information (along with a list of similar movies) in an SQLite3 database.

**main.py** contains the logic for the webapp, which is fired when a user interacts with the app.

&nbsp;

## Page 1: User form

<img align = "right" src="/app-page-one.png" alt="alt text" height ="425" width="950"/>

- The user is first asked to select his/her preferences on movie type, genres and nationality.

&nbsp;

## Page 2: Movies based on user selected categories

<img align = "right" src="/app-page-two.png" alt="alt text" height ="425" width="950"/>

- Based on the user choices, the corresponding movies with the highest Ratings are retrieved from the movie database and they are displayed. 

&nbsp;

## Page 3: Similar Movies using Content-based filtering

<img align = "right" src="/app-page-three.png" alt="alt text" height ="425" width="950" style="margin: 50px"/>

- When the user clicks on one of the movies on Page 2, they are directed to a page containing more information about the specific movie.
- Here, we retrieve the top 5 similar movies with highest Ratings from the database and display them to the user.
- If the user clicks on one of the recommended similar movies, they will be directed to a page containing more information about that movie, along with 5 other similar movies.

## Further Possible Improvements

- Building a scheduled and efficient data pipeline: We can use Airflow to schedule jobs to scrape, preprocess and load data everyday. Furthermore, computing cosine similarity can have O(n^2) time complexity. To make this more efficient, we can either use Locality Sensitive Hashing or use a distributed data processing framework such as Spark.
- As we gather more data with users, if we can collect some sort of feedback (implicit or emplicit), we can possibly improve the recommender algorithm by incorporating Collaborative Filtering.
