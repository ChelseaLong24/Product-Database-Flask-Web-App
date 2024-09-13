from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    data = current_app.config['DATA']


    return render_template('home.html', data=data)
