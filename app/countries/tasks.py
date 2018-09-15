import os
from flask import request, g, url_for
from flask import current_app as app
from app.countries.models import Country
from app.users.models import MembershipPlan
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt


def save_country(country):

    if request.form.get("countryCurrency"):
        country.countryCurrency = request.form['countryCurrency']

    if request.form.get("monthlyAmount"):
        country.monthlyAmount = request.form['monthlyAmount']

    if request.form.get("displayOrder"):
        country.displayOrder = request.form['displayOrder']

    try:
        country_id = country.save()
        return {'country_id': str(country_id.id)}
    except Exception as e:
        return {'error': str(e)}

def transpose_country(country):
    return {
        '_id': str(country.id),
        'countryName': country.CountryName,
        'countryCode': country.CountryCode,
        'countryCurrency': country.countryCurrency,
        'monthlyAmount': float(country.monthlyAmount),
        'displayOrder': country.displayOrder,
        'date_created': country.date_created.isoformat() if country.date_created else '',
        'date_modified': country.date_modified.isoformat() if country.date_modified else ''
    }
