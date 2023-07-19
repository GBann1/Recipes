# Pair programmed by Gordon Bannon and Owen Lang


from flask_app.controllers import controller_recipes, controller_users
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)