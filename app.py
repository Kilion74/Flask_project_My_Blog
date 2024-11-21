from symtable import Class

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog.db'  # Используйте нужный вам URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создайте объект SQLAlchemy
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Создайте таблицы в базе данных


with app.app_context():
    db.create_all()


@app.route('/')
def index():  # put application's code here
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Something went wrong"
    else:
        return render_template('create.html')


# @app.route('/delete', methods=["GET", "POST"])
# def delete():
#     if request.method == "POST":
#         id = request.form['id']
#         post = Post(id=id)
#         try:
#             db.session.delete(post)
#             db.session.commit()
#             return redirect(url_for('index'))
#         except:
#             return "Something went wrong"
#
#     return render_template('delete.html')
@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        id = request.form['id']
        post = Post.query.get(id)  # Извлекаем пост из базы по его идентификатору
        if post:  # Проверяем, существует ли пост
            try:
                db.session.delete(post)  # Удаляем пост
                db.session.commit()  # Сохраняем изменения в базе данных
                return redirect(url_for('index'))  # Перенаправляем на страницу индекса
            except Exception as e:  # Сохраняем ошибку в случае сбоя
                print(e)  # Это поможет вам диагностировать проблему
                return "Something went wrong"
        else:
            return "Post not found"  # Возвращаем сообщение, если пост не найден

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)
