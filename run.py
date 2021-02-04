# This line imports form the __init__.py within that package(flaskblog package) 
# The app variable HAS to exist within __init__.py
from flaskblog import app

if __name__ == '__main__':
	app.run(debug=True)
