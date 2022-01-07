from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.item}-{self.date_created}"


@app.route('/', methods=['GET', 'POST'])
def addToThelist():
    if request.method == 'POST':
        todo = ToDo(item=request.form['itemTodo'])
        if todo.item == "":
            error ="invalid entry.Thank you."
            allTodo = ToDo.query.all()
            return render_template('index.html', allTodo=allTodo, error=error)
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def updatepage(sno):
    error = None
    if request.method == 'POST':
        if request.form['itemTodo'] == '':
            todo = ToDo.query.filter_by(sno=sno).first()
            error ="invalid entry.Try again.Thank you."
            return render_template('edit.html', error=error, todo=todo)
        
        todo = ToDo.query.filter_by(sno=sno).first()    
        todo.item = request.form['itemTodo']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('edit.html',todo=todo)



@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()