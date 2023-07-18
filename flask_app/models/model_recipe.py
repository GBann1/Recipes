from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_user import User

DATABASE = "recipes_db"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        # Use JOIN statement because table requests user NAME not just ID
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for entry in results:
            # recipe_info = {
            #     'id':entry['recipes.id'],
            #     'name':entry['name'],
            #     'description':entry['description'],
            #     'instructions':entry['instructions'],
            #     'under_30':entry['under_30'],
            #     'created_at':entry['recipes.created_at'],
            #     'updated_at':entry['recipes.updated_at'],
            #     'user_id':entry['user_id']
            # }
            current_recipe = cls(entry)
            user_info = {
                'id' : entry['users.id'],
                'first_name' : entry['first_name'],
                'last_name' : entry['last_name'],
                'email' : entry['email'],
                'password' : entry['password'],
                'created_at' : entry['users.created_at'],
                'updated_at' : entry['users.updated_at']
            }
            current_recipe.user = User(user_info)
            recipes.append(current_recipe)
        return recipes
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, {'id':id})
        recipe = cls(result[0])
        for row in result:
            user = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
        recipe.user = User(user)
        return recipe


    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s, %(user_id)s);"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results 
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results 

    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {'id':id})
        return results