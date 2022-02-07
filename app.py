from flask import Flask, render_template,redirect,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
import tkinter
from tkinter import messagebox


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def home():

    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('todo.html',todo_list=todo_list)
@app.route("/add", methods=["POST"])
def add():
    #add new item
    
    title = request.form.get("title")
    if title != "":
        new_todo = Todo(title=title,complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        # This code is to hide the main tkinter window
        root = tkinter.Tk()
        root.withdraw()
        # root.mainloop()

        messagebox.showinfo(title="Alert message", message="Please enter valid input")
        return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))
     
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))



@app.route('/about')
def about():
    return "About page"


if __name__== "__main__":
    db.create_all()
    app.run(debug=True)
