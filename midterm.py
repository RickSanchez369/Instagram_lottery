from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, bcrypt, Users , LotteryType , LotteryEntry
from werkzeug.security import check_password_hash
import os
from selenium import webdriver
from forms import RegistrationForm, LoginForm, LotteryChoiceForm
from data_scraper import login, collect_comments, collect_likes, collect_followers 
from payment import process_payment
import random


# creat app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/theflaskapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'your_default_secret_key')

#connect and creat tabele
db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()


# create routs
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('حساب شما ایجاد شد! اکنون می‌توانید وارد شوید', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('خطایی در ایجاد حساب کاربری شما رخ داد.', 'danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('ورود موفقیت‌آمیز بود!', 'success')
            return redirect(url_for('lottery'))
        else:
            flash('ورود ناموفق. لطفاً ایمیل و پسورد را بررسی کنید', 'danger')
    return render_template('login.html', form=form)


@app.route('/choose_lottery', methods=['GET', 'POST'])
def choose_lottery():
    form = LotteryChoiceForm()
    if form.validate_on_submit():
        chosen_type = form.lottery_type.data
        lotterytype = LotteryType(chosen_type)
        try:
            db.session.add(lotterytype)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('خطایی در انتخاب نوع قرعه کشی رخ داد.', 'danger')
        flash(f'شما {chosen_type} را انتخاب کرده‌اید.', 'success')
        return redirect(url_for('start_lottery',lottery_type=lotterytype))
    return render_template('choose_lottery.html', form=form)

 
@app.route('/start_lottery/<lottery_type>' , method=['GET','POST'])
def start_lottery(lottery_type):
    if request.method == 'POST':
        post_url = request.form['post_url']
        min_mentions = int(request.form['min_comments'])
        
        driver = webdriver.Chrome(executable_path='C:\\Users\\Almas\\Desktop\\chromedriver-win64\\chromedriver.exe')
        login(driver)
        
        if lottery_type == 'comments':
            comments = collect_comments(driver,post_url)
            winner = random.choice(comments)
        elif lottery_type == 'likes':
            likes =collect_likes(driver,post_url)
            winner = random.choice(likes)
        elif lottery_type == 'followers':
            followers = collect_followers(driver, post_url)
            winner=random.choice(followers)
        elif lottery_type == 'score':
            scores =collect_comments(driver,post_url, min_mentions)
        else:
            flash('Invalid lottery type selected!')
            return redirect(url_for('start_lottery'))
        
        return redirect(url_for('lottery_result', winner=winner))
   
    return render_template('lottery.html')


@app.route('/lottery_result')
def lottery_result(winner):
    return render_template('lottery_result.html' ,winner)






# run app
if __name__ == "__main__":
    app.run(debug=True)
