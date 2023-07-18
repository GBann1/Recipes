from flask_app import app
from flask import render_template, redirect, request

from flask_app.models.model_recipe import Recipe


@app.route('/recipe/new')
def recipe_new():
    return render_template("new_recipe.html")

@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    data = {
        **request.form
    }
    Recipe.create(data)
    return redirect('/')

@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    Recipe.delete_one(id)
    return redirect('/dashboard/')

@app.route('/show_recipes/<int:id>')
def show_recipe(id):
    recipe = Recipe.get_one(id)
    return render_template('show_recipe.html', recipe = recipe)
