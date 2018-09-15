import os
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.countries.models import Country
from app.auth.models import login_required, admin_required
from app.countries.tasks import transpose_country,save_country
from app.commons.utils import update_document


countries = Blueprint('countries_blueprint', __name__,
                    url_prefix='/api/countries')

@countries.route('/countries')

@countries.route('', methods=['POST'])
#@admin_required
def create_country():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    country = Country()
    try:
        save_response = save_country(country)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['country_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})


@countries.route('')
def read_countries():
    """
    find list of categories for the agent
    :return:
    """
    countries = Country.objects.order_by('displayOrder','CountryName')
    if not countries:
        return build_response.build_json([])

    response_countries = []

    for country in countries:
        obj_country = transpose_country(country)
        response_countries.append(obj_country)

    return build_response.build_json(response_countries)

#@login_required
@countries.route('/findcountries')
def find_countries():
    """
    find list of countries for the agent
    :return:
    """
    page_nb = int(request.args.get('pageNumber'))

    items_per_page = int(request.args.get('pageSize'))

    offset = (page_nb - 1) * items_per_page if page_nb > 0 else 0

    countries = Country.objects()
    
    if request.args.get('name'):
        countries = countries.filter(CountryName__iexact=request.args.get('name'))

    if not countries:
        return build_response.build_json([])

    countries = countries.order_by('displayOrder','CountryName')
    #countries = skip( offset ).limit( items_per_page )

    response_countries = []

    for country in countries:
        obj_country = transpose_country(country)
        response_countries.append(obj_country)

    return build_response.build_json({"payload":response_countries})

@countries.route('/<id>')
def read_country(id):
    """
    Find details for the given country id
    :param id:
    :return:
    """
    try:
        country = Country.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_country(country))


@countries.route('/<id>', methods=['PUT'])
def update_country(id):
    country = Country.objects.get(id=ObjectId(id))
    try:
        save_response = save_country(country)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['country_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})



@countries.route('/<id>', methods=['DELETE'])
def delete_country(id):
    """
    Delete a country
    :param id:
    :return:
    """
    try:
        country = Country.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    country.delete()
    return build_response.sent_ok()
