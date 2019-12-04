#!/usr/bin/env python3

# Russell Felts
# Flask Mailroom Assignment 01

""" Main """

import os
# import base64

from flask import Flask, render_template, request, redirect, url_for #, session

from model import Donation, Donor

APP = Flask(__name__)


@APP.route('/')
def home():
    """
    Display the home page
    :return: The all donations page
    """
    return redirect(url_for('all'))


@APP.route('/donations/', methods=['GET', 'POST'])
def all():
    """
    Display a list of all the donations
    :return: The all donations page
    """
    if request.method == 'POST':
        donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
        print("Donor ID ", donor.id)
        donations = Donation.select().where(Donation.donor_id == donor.id)
        print("Dontation", donations)
        return render_template('donations.jinja2', donations=donations)

    donations = Donation.select()
    print("All donations ", donations)
    return render_template('donations.jinja2', donations=donations)


@APP.route('/create', methods=['GET', 'POST'])
def create(message=None):
    """
    Adds a new donation.
    For a Post request submit the donation info otherwise display the create donation page.
    Based on the donor info validity display and error with the create page or the all
    donations page.
    :return: The created donation or the all donations page
    """

    # Get the variable message from the request
    message = request.args.get('message')
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
            donation = Donation(value=request.form['donation_amount'], donor_id=donor.id)
            donation.save()
            return redirect(url_for('home'))
        except Donor.DoesNotExist:
            return redirect(url_for('new_donor'))
        except ValueError:
            message = "Please add a donation amount for donor {}".format(donor.name)
            return render_template('create.jinja2', message=message)

    return render_template('create.jinja2', message=message)


@APP.route('/donor', methods=['GET', 'POST'])
def new_donor():
    """
    Add a new donor to the Donor table
    :return: The create donor or create donation page
    """
    if request.method == 'POST':
        donor = Donor(name=request.form['donor_name'])
        donor.save()
        message = "The donor {} was created. Do you want to add a donation amount".format(donor.name)
        # Pass the variable message to the create function
        return redirect(url_for('create', message = message))

    return render_template('donor.jinja2')


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 6738))
    APP.run(host='0.0.0.0', port=PORT)
