from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import engine 
import sqlite3

# path = 'E:/company_specific/innvonix/test.db'
# conn = sqlite3.connect(path)
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(1000))
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=["GET","POST"])
def home_page():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        all_tasks=Todo.query.all()
    else:
        all_tasks=Todo.query.all()
    return render_template('index.html',all_t=all_tasks)

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        update_query=Todo.query.filter_by(sno=sno).first()
        
        update_query.title=title
        update_query.desc=desc
        db.session.add(update_query)
        db.session.commit()
        return redirect("/")
    else:
        update_query=Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', update_q=update_query)



@app.route('/delete/<int:sno>')
def delete(sno):
    deleted_query=Todo.query.filter_by(sno=sno).first()
    db.session.delete(deleted_query)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)