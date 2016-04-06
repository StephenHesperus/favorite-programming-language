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
   Now QuestionForm.validate_on_submit() part has problems entering.

4. After the first version, apparently it doesn't exactly match the flow control chart. So I added another version, and to make rendering form field easier, I used a macro from the web.

## Comparison

After I finished my project, now it's time to compare my version to Miguel Grinberg's.
His version uses lists instead of database. And the control flow is slightly different there. But I think they both do the job.

## Beyond A Working Prototype

Seems like I always just right a program, and I don't have the habit of writing tests nor documentation. I guess part of the reason is of where I learnt programming. I never took a real course, everything I learnt, I mostly learnt from the internet, I do read books, but mostly electronic version. I guess if I really want to take programming seriously, I should starting doing them.

And it's true for a lot of things I guess. For example, typing habit, writing habit etc..

## Coming Back Again

This is the date when I come back for testing and documentation: Thu Mar 17 15:05:12 CST 2016. I guess I really don't know how to do testing or documentation.

## All The Tests Are Done

After the tests, it's documentation and refactor.
