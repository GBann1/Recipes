# Pair programmed by Gordon Bannon and Owen Lang
# Date: 7/18/23
# Note: View Recipe and Edit routes do not work


from flask_app.controllers import controller_recipes, controller_users
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)