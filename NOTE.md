# Favorite Programming Language Progress

1. The very beginning. I just created a virtualenv for the project using virtualenvwrapper. I think I will install the flask package now.

2. Now I will create the app.py file. Create basic app and templates.
   When I create template file index.html, the url for starting the game is uncertain, I remember it's under url '/question' in the example, and that's what I use here.
   Now, I'm creating question.html. The problem comes as I don't know too much about WTForms, so I need to install the flask extension and read the document.
   Maybe I need to create the form first.
   Now I need to find a software to draw the control flow.
   Using Lucidchart from Chrome app store, I draw the control flow:
   ![application control flow chart](./app-control-flow-char.svg)

3. After I created the flow chart, I think I need to build the database models. So I installed flask-sqlalchemy.
   I just create the LanguageTest model, and GuessGame class to do game logic.
   Now QuestionForm.validate_on_sumbit() part has problems entering.
