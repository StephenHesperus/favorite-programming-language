from . import create_app


app = create_app('heroku')
app.run()
