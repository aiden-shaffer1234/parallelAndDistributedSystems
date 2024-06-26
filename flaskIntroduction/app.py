from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addReview')
def addReview():
        return render_template("addReview.html")


@app.route('/addrev', methods = ['POST', 'GET'])
def addrev():
    if request.method == 'POST':
        try:
            title = request.form['Title']
            director = request.form['Director']
            year = request.form['Year']
            genre = request.form['Genre']
            review = request.form['Review']
            rating = request.form['Rating']
            MovieID = title[:5] + str(year)

            #need to check if the movie is unique
            with sql.connect("movieData.db") as con:
                cursor = con.cursor()

                #check if it exists, if not then add it 
                cursor.execute("SELECT * FROM Movies WHERE MovieID = ?", (MovieID,))
                existing_row = cursor.fetchone()

                if not existing_row: 
                    cursor.execute("INSERT INTO Movies (MovieID , Title , Director, Genre, Year) VALUES (?,?,?,?,?)",
                    (MovieID, title, director, genre, year))
                    print("movie successfully added")

                #add the review
                cursor.execute("SELECT DATETIME('now')")
                cur_time = cursor.fetchone()[0]

                print("adding review...")
                cursor.execute("INSERT INTO Reviews (Username , MovieID , ReviewTime , Rating , Review ) VALUES (?,?,?,?,?)",
                (title, MovieID, cur_time, rating, review))

                print("Review successfully added")
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template("index.html") #check
            con.close()

@app.route('/getReviews')
def getReviews():
    return render_template("getReviews.html")
    

@app.route('/listByGenre', methods = ['POST', 'GET'])
def listByGenre():
    if request.method == "POST":
        genre = request.form["Genre"]
        con =  sql.connect("movieData.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        # select movies in the genre from movies then get thier ratings in reviews table
        cur.execute("SELECT Movies.Title, Movies.Director, Reviews.Review, Reviews.Rating FROM Movies INNER JOIN Reviews on Movies.MovieID = Reviews.MovieID WHERE Genre = ?", (genre,))
        rows = cur.fetchall()
        return render_template("listByGenre.html", Genre = genre, rows = rows)



@app.route('/getYear')
def getYear():
    return render_template("getYear.html")

@app.route('/topfive', methods = ['POST', 'GET'])
def top_five():
    if request.method == "POST":
        year = request.form["Year"]
        con = sql.connect("movieData.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        cur.execute("SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS AverageRating FROM Movies INNER JOIN Reviews ON Movies.MovieID = Reviews.MovieID WHERE Movies.Year = ? GROUP BY Movies.MovieID ORDER BY AverageRating DESC", (year,))
        rows = cur.fetchmany(5)
        print(rows)
        return render_template("bestInYear.html", Year = year, rows = rows)

if __name__ == '__main__':
    app.run(debug = True)
    