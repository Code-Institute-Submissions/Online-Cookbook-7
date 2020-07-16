import os

from os import path
if path.exists('env.py'):
    import env

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo #import pymongo library
from bson.objectid import ObjectId #importing from BSON library

# flask uses import name to know where to look for templates, resources etc
app = Flask(__name__)

# Connect to database
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Create instance of PyMongo
mongo = PyMongo(app)

@app.route('/')

# Connect Read all Recipes file
@app.route('/get_recipes')
def get_recipes():
    return render_template("all_recipes.html", recipes=mongo.db.recipes.find())

# Connect to Create/Add recipes to database file
@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")

# Connect to Update Recipes file
@app.route('/update_recipe')
def update_recipe():
    return render_template("edit.html", categories=mongo.db.categories.find(),
    recipes=mongo.db.recipes.find())

# Post new recipe to database
@app.route('/new_recipe', methods=['POST'])
def new_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

# Edit recipes button connect
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipes_id):
    the_recipe = mongo.db.recipes.find_one({"_id: ObjectId(recipes_id)"})
    all_categories = mongo.db.categories.find()
    return render_template('edit.html', recipe=the_recipe, categories=all_categories)

    

# Set PORT and IP Address
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)