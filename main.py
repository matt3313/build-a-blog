
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.String(500))

    def __init__(self, title, text):
        self.title = title
        self.text = text


@app.route("/blog")
def blog():
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('single-blog.html', title="Build-a-Blog", blog=blog)

    blogs = Blog.query.all()

    return render_template("blog.html", title = "Build-a-Blog", blogs = blogs)


@app.route("/newpost", methods = ['GET', 'POST'])
def newpost():

    
    if request.method == 'POST':
        
        new_title = request.form['title']
        new_text = request.form['text']
        
        title_error = ''
        text_error = ''
        
        if len(new_title) < 1:
            title_error = 'Please enter a title'

        if len(new_text) < 1:
            text_error = 'Please enter text'
        
        if not text_error and not title_error:
            new_blog = Blog(new_title, new_text)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = str(new_blog.id)
            query_str = '/blog?id=' + blog_id
            return redirect(query_str)

        else:
            return render_template('newpost.html', title_error = title_error, text_error = text_error, new_text = new_text)
        
    else:
        return render_template("newpost.html", title = 'Build-a-Blog')



if __name__ == '__main__':
    app.run()