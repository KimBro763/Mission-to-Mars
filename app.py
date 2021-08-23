from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set up flask
app = Flask(__name__)

#tell python how to connect to mongo using pymongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

## Set Up App Routes

#html page route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


#set up scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

#tell Flask to run
if __name__ == "__main__":
    app.run()
