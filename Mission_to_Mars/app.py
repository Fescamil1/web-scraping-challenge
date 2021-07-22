#import dependencies and scrape function
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app=Flask(__name__)

# mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars_data

    # call the scrape function
    mars_data = scrape_mars.scrape_info()

    # update the Mongo DB
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
