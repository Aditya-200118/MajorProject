import secrets
import os
from tkinter.messagebox import NO
from PIL import Image
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from app.helpers import apology, lookup
from flask import Blueprint, flash
from app.extensions import DB, bcrypt
from app.models import User, Portfolio, Stock_Transaction
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, QuoteForm, BuyForm, SellForm
from sqlalchemy import TEXT
server_bp = Blueprint('main', __name__, static_folder="\\static", template_folder="\\templates")


# gets the current username
def get_user():
    user_id = session.get("user_id")
    print(user_id)
    user_name = DB.execute("SELECT username FROM users WHERE id = ?", user_id)
    print(user_name)
    username = (user_name[0])
    username = username['username']
    return username


def get_shares(x):
    # shares = DB.execute("SELECT quantity FROM ? as quantity WHERE stock like ?", get_user() + '_portfolio', x)
    check = DB.session.query(Portfolio.quantity).filter_by(stock = x, user_id = current_user.id)
    for row in check:
        check = row.quantity    
    return int(check)


# gets the cash left in the users trading account
def get_cash():
    """ GETS BALANCE FROM USERS ACCOUNT """
    query = DB.session.query(User).filter_by(id = current_user.id)
    for row in query:
        cash = row.cash
    return float(cash)


def get_count():
    count = DB.session.query(Stock_Transaction.stock).filter_by(user_id=current_user.id).count()  # returns an integer
    return int(count)



def get_stock():
    stocks = []
    # data = DB.execute("SELECT stock FROM ?", get_user() + '_transaction')
    data = DB.session.query(Stock_Transaction.stock).filter_by(user_id = current_user.id).all()
    # data_list = [i for s in [d.value() for d in data] for i in s]
    # stocks = [d['stock'] for d in data if "stock" in d]
    # return stocks
    for row in data:
        stocks.append(row.stock)
    return stocks


def get_stock_portfolio():
    stocks = []
    # data = DB.execute("SELECT stock FROM ?", get_user() + '_portfolio')
    data = DB.session.query(Portfolio.stock).filter_by(user_id = current_user.id).all()
    # stocks = [d['stock'] for d in data if "stock" in d]
    for row in data:
        stocks.append(row.stock)
    return stocks


def get_price():
    prices = []
    # data = DB.execute("SELECT price FROM ?", get_user() + '_transaction')
    data = DB.session.query(Stock_Transaction.price).filter_by(user_id = current_user.id).all()
    # data_list = [i for s in [d.value() for d in data] for i in s]
    # prices = [d['price'] for d in data if "price" in d]
    for row in data:
        prices.append(float(row.price))
    return prices


def get_quantity():
    quantity = []
    # data = DB.execute("SELECT quantity FROM ?", get_user() + '_transaction')
    data = DB.session.query(Stock_Transaction.quantity).filter_by(user_id = current_user.id).all()
    # data_list = [i for s in [d.value() for d in data] for i in s]
    for row in data:
        quantity.append(int(row.quantity))
    return quantity


def get_transactions():
    transactions = []
    # data = DB.execute("SELECT Transactions FROM ?", get_user() + '_transaction')
    data = DB.session.query(Stock_Transaction.transaction_time).filter_by(user_id = current_user.id)
    # data_list = [i for s in [d.value() for d in data] for i in s]
    for row in data:
        transactions.append(row.transaction_time)
    return transactions

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(server_bp.root_path, 'static/profile', picture_fn)
    
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@server_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", footer = False, form = form, color = "#1E293B")

@server_bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    logout_user()
    # Redirect user to login form
    return redirect(url_for("main.login"))
    # return render_template("login.html")


@server_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email=form.email.data, password = hashed_password)
        DB.session.add(user) 
        DB.session.commit()
        flash(f'Your account has been created with username {form.username.data}!', category='success')
        return redirect(url_for('main.login'))
    return render_template("register.html", footer = False, form = form, color = "#1E293B")

@server_bp.route("/quote", methods=["GET", "POST"]) # @login_required
@login_required
def quote():
    
    form = QuoteForm()
    symbol = form.symbol.data
    if form.validate_on_submit():
        if (lookup(symbol)) == None:
            flash("Enter correct stock symbol", "danger")
            return redirect(url_for("main.quote"))        
        data = lookup(symbol)
        data = data['price']
        
        return render_template('quoted.html', data=data, symbol=symbol)
    return render_template("quote.html", form = form, color = "#1E293B")

@server_bp.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form_picture=form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        DB.session.commit()

        flash('Your account has been updated', 'success')

        return redirect(url_for('main.account'))

    elif request.method == "GET":

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile/' + current_user.image_file)
    return render_template("account.html", image_file = image_file, footer = False, form = form, color = "#1E293B")


@server_bp.route("/")
@login_required
def index():
    count =int(DB.session.query(Portfolio.stock).distinct('stock').filter_by(user_id=current_user.id).count())  # returns an integer

    stock = DB.session.query(Portfolio.stock).filter_by(user_id = current_user.id).all()
    stocks = []
    for s in stock:
        stocks.append(str(s.stock))

    price = DB.session.query(Portfolio.price).filter_by(user_id = current_user.id).all()
    prices = []
    for p in price:
        prices.append(float(p.price))

    quantity = DB.session.query(Portfolio.quantity).filter_by(user_id = current_user.id).all()
    quantities = []
    for q in quantity:
        quantities.append(int(q.quantity))
    
    totals = [] 
    total =  DB.session.query(Portfolio.quantity*Portfolio.price).filter_by(user_id = current_user.id).all()
    for t in total:
        totals.append(float(t[0]))

    grand_total = 0
    for x in range(0, len(totals)):
        grand_total = grand_total + totals[x]
    grand_total = grand_total + get_cash()
    
    return render_template('index.html', price=prices, stocks=stocks, quantity=quantities, counts=count, total=totals, current=get_cash(), grand_total=grand_total, footer = False, color = "#1E293B")

@server_bp.route("/buy", methods = ["GET", "POST"])
@login_required
def buy():
    form = BuyForm()

    symbol = str(form.symbol.data).upper()
    if form.validate_on_submit():
        if (lookup(symbol)) == None:
            flash("Enter correct stock symbol", "danger")
            return redirect(url_for("main.buy"))     
        if form.quantity.data == str:
            flash("Enter correct quantity", 'danger')
            return redirect(url_for("main.buy")) 

        qty = int(form.quantity.data)      

        data = lookup(symbol)
        price = data['price']

        amount = qty*float(price)
        if get_cash() < amount:
            flash("Don't have enough cash to buy the stock.", 'info')
            return redirect(url_for('main.buy'))
        else:
            balance = get_cash() - amount
            value = DB.session.execute("SELECT EXISTS(SELECT stock FROM portfolio WHERE stock LIKE :y AND user_id = :z) as value", {'y': symbol,'z': current_user.id } )
            for row in value:
                row = row['value']
            if row == 0:
                buy = Portfolio(stock = str(symbol), quantity = qty, price = price, user_id = current_user.id)
                transaction = Stock_Transaction(stock = str(symbol), quantity = qty, price = price, user_id = current_user.id)
                DB.session.execute("UPDATE user SET cash = :x WHERE id = :y", {'x':balance, 'y': current_user.id})
                DB.session.add(buy)
                DB.session.add(transaction)
                DB.session.commit()
                flash('Shares have been bought, amount deducted from account.', 'info')
                return redirect(url_for("main.buy"))
            elif row == 1:
                # current_quantity = DB.execute("SELECT quantity FROM ? where stock like ?", table_name, to_buy.upper())
                current_quantity = DB.session.query(Portfolio.quantity).filter_by(stock = symbol, user_id = current_user.id)
                for row in current_quantity:
                    current_qty = row.quantity
                new_quantity = int(current_qty) + int(qty)

                current_price = DB.session.query(Portfolio.price).filter_by(stock = symbol, user_id = current_user.id)
                for row in current_price:
                    current_pie = float(row.price)
                avg_price = (float(current_pie) + float(price))/2

                DB.session.execute("UPDATE portfolio SET quantity = :y, price = :z where stock LIKE :s AND user_id = :id", {
                    'y': int(new_quantity),
                    'z': avg_price,
                    's': str(symbol),
                    'id': current_user.id
                    })
                transaction = Stock_Transaction(stock = str(symbol), quantity = qty, price = price, user_id = current_user.id)

                DB.session.add(transaction)
                DB.session.commit()
                flash('Shares have been bought, amount deducted from account.', 'info')
                return redirect(url_for('main.buy'))
        print(current_user.id, current_user.username, current_user.email)    
        form.symbol.data = None
        form.quantity.data = None
    return render_template("buy.html", form = form, color = "#1E293B")


@server_bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    form = SellForm()

    symbol = str(form.symbol.data).upper()
    if form.validate_on_submit():
        if (lookup(symbol)) == None:
            flash("Enter correct stock symbol", "danger")
            return redirect(url_for("main.buy"))     
        if form.quantity.data == str:
            flash("Enter correct quantity", 'danger')
            return redirect(url_for("main.buy")) 

        qty = int(form.quantity.data) 

        data = lookup(symbol)
        price = data['price']

        amount = qty*float(price)

        if int(qty) < 1:
            flash ("Enter correct quantity.", 'danger')

        if get_shares(symbol) < float(qty):
            flash("You don't have that many shares.", 'danger')
            return redirect(url_for('main.sell'))
        else:
            current_quantity = DB.session.query(Portfolio.quantity).filter_by(stock = symbol, user_id = current_user.id)
            for row in current_quantity:
                 current_qty = row.quantity

            new_quantity = float(current_qty) - float(qty)

            if new_quantity == 0:
            
                DB.session.execute("DELETE FROM portfolio WHERE STOCK LIKE :x and user_id = :y ", {'x': symbol, 'y': current_user.id})
            else:
                DB.session.execute("UPDATE portfolio SET Quantity = :x where STOCK LIKE :y and user_id = :z", {'x': new_quantity, 'y': symbol, 'z': current_user.id})
    
            transaction = Stock_Transaction(stock = str(symbol), quantity = qty, price = price, user_id = current_user.id)
            balance = get_cash() + amount
            DB.session.execute("UPDATE user SET cash= :x WHERE id= :id", {'x': balance, 'id': current_user.id})
            DB.session.add(transaction)
            DB.session.commit()
            flash('Shares have been sold, amount added to account.', 'info')
            return redirect(url_for("main.index"))
    else:
        form.symbol.data = None
        form.quantity.data = None
        return render_template("sell.html", stocks=get_stock_portfolio(), form = form, footer = False, color = "#1E293B")


@server_bp.route("/history")
@login_required
def history():
    return render_template("history.html", counts=get_count(), stocks=get_stock(),
    price=get_price(), 
    quantity=get_quantity(), transactions=get_transactions(), footer = False, color = "#1E293B")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    server_bp.errorhandler(code)(errorhandler)