from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blogs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    blogtext = db.Column(db.String(500))


    def __init__(self, title, blogtext):
        self.title = title
        self.blogtext = blogtext


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title_name = request.form['title']
        blogtext_name = request.form['blogtext']
        new_entry = Blogs(title_name,blogtext_name)
        db.session.add(new_entry)
        db.session.commit()

    tasks = Blogs.query.all()
    return render_template('todos.html', title='Build a Blog', tasks=tasks)


@app.route('/delete-task', methods=['POST'])
def delete_blog():

    task_id = int(request.form['task-id'])
    task = Blogs.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()