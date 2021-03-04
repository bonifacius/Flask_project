from flask import Flask, render_template, request, redirect
# импоритруем бд
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настраиваем БД и называем ее shop.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
# Чтобы выполнять настройки с базой данных
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# Создаем объект с параметром нашего приложения app
db = SQLAlchemy(app)

# Создаем таблицу
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title




# Прописывем функции которые отслеживают переходы на разные url
# Создаем декоратор для главной страницы
@app.route('/')
def index():
    # Сделаем вывод добавленных товаров на странице index
    # 1. Создадим объект items
    items = Item.query.order_by(Item.price).all()
    # 2. Вторым параметром прописываем нашу  переменную с элементами из базы данных
    return render_template("index.html", data=items)

@app.route('/about')
def about():
    return render_template("about.html")

# Добавляем динамический параметр <int>:
@app.route('/buy/<int:id>')
def item_buy(id):
    return str(id)

@app.route('/create', methods=['POST','GET'])
def create():
    # Если данные отправляются через POST мы будем получать и добавлять новую запись

    if request.method == 'POST':
    # 1. Получили данные из формы input
    # 2. Записывються в переменные
        title = request.form['title']
        price = request.form['price']
    # 3. Создается объект класса Item
        item = Item(title=title, price=price)
    # 4. Сохраняем этот объект как новую запись для таблицы
        try:
            db.session.add(item)
            # выполняем добавление
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка! Возможно какое-то поле не заполнено"



    else:
        return render_template("create.html")



if __name__ == "__main__":
    app.run(debug=True)






