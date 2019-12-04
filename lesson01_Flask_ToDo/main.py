#!/usr/bin/env python3

# Russell Felts
# Flask To Do Activity 01

""" Main """

from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

APP = Flask(__name__)
APP.secret_key = os.environ.get('SECRET_KEY').encode()


@APP.route('/all')
def all_tasks():
    """
    Display the all task page
    :return: The all task url
    """
    return render_template('all.jinja2', tasks=Task.select())


@APP.route('/create', methods=['GET', 'POST'])
def create():
    """
    Verify the user is logged in or display the login page before proceeding.
    For a Post request submit the task info then display the all task page.
    Otherwise display the create task page.
    :return: The create task or all task page
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        task = Task(name=request.form['task_name'])
        task.save()

        return redirect(url_for('all_tasks'))

    return render_template('create.jinja2')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    For a Post request submit the login info otherwise display the login page.
    Based on the login info validity display and error with the login page or
    the all task page.
    :return: The login or all task page
    """
    if request.method == 'POST':
        try:
            user = User.select().where(User.name == request.form['user_name']).get()
            if user and pbkdf2_sha256.verify(request.form['password'], user.password):
                print("In login user passowrd check")
                session['username'] = request.form['user_name']
                return redirect(url_for('all_tasks'))
            return render_template('login.jinja2', error="Incorrect username or password.")
        except User.DoesNotExist:
            return render_template('login.jinja2', error="Incorrect username or password.")

    return render_template('login.jinja2')


@APP.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    """
    Base on the user's login status display the login page or the incomplete
    task page.
    :return: The login or incomplete task page
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.select().where(User.name == session['username']).get()

        Task.update(performed=datetime.now(), performed_by=user)\
            .where(Task.id == request.form['task_id'])\
            .execute()

    return render_template('incomplete.jinja2', tasks=Task.select().where(Task.performed.is_null()))


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT)
