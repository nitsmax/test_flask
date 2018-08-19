import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.users.models import User, MembershipPlan
from app.auth.models import login_required, admin_required
from app.users.tasks import transpose_user
from app.commons.utils import update_document
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


users = Blueprint('users_blueprint', __name__,
                    url_prefix='/api/users')

@users.route('/membershipplans')
#@admin_required
def get_membershipplans():
    '''
    For inserting the categories
    '''

    plans = [['Free','Free Membership. No Amount Charged', 0], ['Monthly','Monthly Amount will be charges',200], ['Annually','Annully Amount will be charges',1000]]
    for plan in plans:
        membershipP = MembershipPlan()
        membershipP.name = plan[0]
        membershipP.description = plan[1]
        membershipP.amount = plan[2]
        membershipP.save()

    return build_response.sent_ok()

    '''
    #Get Single Membership
    MembershipP = MembershipPlan.objects(name='Free').get()
    print(MembershipP.name)
    return build_response.sent_ok()
    '''

    membershipPlans = MembershipPlan.objects().order_by('name')
    if not membershipPlans:
        return build_response.build_json([])
    #return build_response.sent_json(users.to_json())

    response_membershipPlans = []

    for membershipP in membershipPlans:
        obj_membershipP = {
            '_id': str(membershipP.id),
            'name': membershipP.name,
            'description': membershipP.description,
            'amount': membershipP.amount,
            'date_created': membershipP.date_created.isoformat(),
            'date_modified': membershipP.date_modified.isoformat()
        }
        response_membershipPlans.append(obj_membershipP)
    #return build_response.build_json(membershipPlans)
    return build_response.sent_json(membershipPlans.to_json())


@users.route('', methods=['POST'])
@admin_required
def create_user():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    user = User()

    # check if the post request has the file part
    if 'Image' in request.files:
        print(request.files)
        file = request.files['Image']
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user.imagefile = filename

    
    user.firstName = request.form['firstName']
    user.lastName = request.form['lastName']
    user.email = request.form['email']
    user.password = generate_password_hash(request.form['password'])

    '''
    content = request.get_json(silent=True)

    user = User()
    user.firstName = content.get("firstName")
    user.lastName = content.get("lastName")
    user.email = content.get("email")
    user.password = generate_password_hash(content.get("password"))
    '''
    
    try:
        user_id = user.save()
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json({
        "_id": str(user_id.id)
    })


@users.route('')
#@admin_required
def read_users():
    """
    find list of users
    :return:
    """
    '''
    users = User.objects().order_by('lastName')
    return build_response.sent_json(users.to_json())
    '''

    users = User.objects()
    if request.args.get('firstName'):
        users = users.filter(firstName__istartswith=request.args.get('firstName'))

    if request.args.get('lastName'):
        users = users.filter(lastName__istartswith=request.args.get('lastName'))

    if request.args.get('email'):
        users = users.filter(email__istartswith=request.args.get('email'))

    if request.args.get('membership'):
        membershipP = MembershipPlan.objects(name__iexact=request.args.get('membership')).get()
        users = users.filter(MembershipPlan=membershipP)


    if not users:
        return build_response.build_json([])

    response_users = []

    for user in users:
        obj_user = transpose_user(user)
        response_users.append(obj_user)

    return build_response.build_json(response_users)



@users.route('/<id>')
@login_required
def read_user(id):
    """
    Find details for the given user id
    :param id:
    :return:
    """
    '''return Response(response=dumps(
        User.objects.get(
            id=ObjectId(
                id)).to_mongo().to_dict()),
        status=200,
        mimetype="application/json")'''

    try:
        user = User.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_user(user))


@users.route('/<id>', methods=['PUT'])
def update_user(id):
    """
    Update a story from the provided json
    :param intent_id:
    :param json:
    :return:
    """
    json_data = loads(request.get_data().decode('utf-8'))
    user = User.objects.get(id=ObjectId(id))
    user = update_document(user, json_data)
    user_id.save()
    return 'success', 200


@users.route('/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete a intent
    :param id:
    :return:
    """
    Intent.objects.get(id=ObjectId(id)).delete()

    try:
        train_models()
    except BaseException:
        pass

    # remove NER model for the deleted stoy
    try:
        os.remove("{}/{}.model".format(app.config["MODELS_DIR"], id))
    except OSError:
        pass
    return build_response.sent_ok()


