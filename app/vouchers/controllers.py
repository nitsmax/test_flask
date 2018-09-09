import os
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.vouchers.models import Voucher
from app.auth.models import login_required, admin_required
from app.voucher.tasks import transpose_voucher,save_voucher
from app.commons.utils import update_document


vouchers = Blueprint('vouchers_blueprint', __name__,
                    url_prefix='/api/vouchers')

@vouchers.route('/vouchers')
#@admin_required
def get_vouchers():
    '''
    For inserting the categories
    '''

    '''plans = [['Free','Free Membership. No Amount Charged', 0], ['Monthly','Monthly Amount will be charges',200], ['Annually','Annully Amount will be charges',1000]]
    for plan in plans:
        membershipP = MembershipPlan()
        membershipP.name = plan[0]
        membershipP.description = plan[1]
        membershipP.amount = plan[2]
        membershipP.save()

    return build_response.sent_ok()

    #Get Single Membership
    MembershipP = MembershipPlan.objects(name='Free').get()
    print(MembershipP.name)
    return build_response.sent_ok()
    '''
    
    membershipPlans = MembershipPlan.objects().order_by('name')
    '''
    if not membershipPlans:
        return build_response.build_json([])
    #return build_response.sent_json(vouchers.to_json())
    '''
    response_membershipPlans = []

    for membershipP in membershipPlans:
        obj_membershipP = {
            '_id': str(membershipP.id),
            'name': membershipP.name,
            #'description': membershipP.description,
            #'amount': membershipP.amount,
            'date_created': membershipP.date_created.isoformat(),
            'date_modified': membershipP.date_modified.isoformat()
        }
        response_membershipPlans.append(obj_membershipP)

    #return build_response.build_json(response_membershipPlans)
    return build_response.sent_json(membershipPlans.to_json())


@vouchers.route('', methods=['POST'])
@admin_required
def create_voucher():
    """
    Create a story from the provided json
    :param json:
    :return:
    """
    voucher = Voucher()
    try:
        save_response = save_voucher(voucher)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['emoji_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})

@vouchers.route('')
#@admin_required
def read_vouchers():
    """
    find list of vouchers
    :return:
    """
    '''
    vouchers = User.objects().order_by('lastName')
    return build_response.sent_json(vouchers.to_json())
    '''

    vouchers = User.objects()
    if request.args.get('firstName'):
        vouchers = vouchers.filter(firstName__istartswith=request.args.get('firstName'))

    if request.args.get('lastName'):
        vouchers = vouchers.filter(lastName__istartswith=request.args.get('lastName'))

    if request.args.get('email'):
        vouchers = vouchers.filter(email__istartswith=request.args.get('email'))

    if request.args.get('membership'):
        membershipP = MembershipPlan.objects(name__iexact=request.args.get('membership')).get()
        vouchers = vouchers.filter(MembershipPlan=membershipP)


    if not vouchers:
        return build_response.build_json([])

    response_vouchers = []

    for voucher in vouchers:
        obj_voucher = transpose_voucher(voucher)
        response_vouchers.append(obj_voucher)

    return build_response.build_json(response_vouchers)



@vouchers.route('/<id>')
#@login_required
def read_voucher(id):
    """
    Find details for the given voucher id
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
        voucher = User.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_voucher(voucher))


@vouchers.route('/<id>', methods=['PUT'])
def update_voucher(id):
    """
    Update a story from the provided json
    :param intent_id:
    :param json:
    :return:
    """
    json_data = loads(request.get_data().decode('utf-8'))
    voucher = User.objects.get(id=ObjectId(id))
    voucher = update_document(voucher, json_data)
    voucher_id.save()
    return 'success', 200


@vouchers.route('/<id>', methods=['DELETE'])
def delete_voucher(id):
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


