import os
from bson.objectid import ObjectId
from flask import Blueprint, request, Response, g
from flask import current_app as app
from app.commons import build_response
from app.vouchers.models import Voucher
from app.auth.models import login_required, admin_required
from app.vouchers.tasks import transpose_voucher,save_voucher
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
#@admin_required
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
                "_id": str(save_response['voucher_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})


#@login_required
@vouchers.route('/findvouchers')
def find_vouchers():
    """
    find list of vouchers for the agent
    :return:
    """
    page_nb = int(request.args.get('pageNumber'))

    items_per_page = int(request.args.get('pageSize'))

    offset = (page_nb - 1) * items_per_page if page_nb > 0 else 0

    vouchers = Voucher.objects()
    if request.args.get('name'):
        vouchers = vouchers.filter(name__iexact=request.args.get('name'))

    if request.args.get('code'):
        vouchers = vouchers.filter(code__icontains=request.args.get('code'))


    if not vouchers:
        return build_response.build_json([])

    vouchers = vouchers.order_by('-date_modified')
    #vouchers = skip( offset ).limit( items_per_page )

    response_vouchers = []

    for voucher in vouchers:
        obj_voucher = transpose_voucher(voucher)
        response_vouchers.append(obj_voucher)

    return build_response.build_json({"payload":response_vouchers})

@vouchers.route('/<id>')
def read_voucher(id):
    """
    Find details for the given voucher id
    :param id:
    :return:
    """
    try:
        voucher = Voucher.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    return build_response.build_json(transpose_voucher(voucher))


@vouchers.route('/<id>', methods=['PUT'])
def update_voucher(id):
    voucher = Voucher.objects.get(id=ObjectId(id))
    try:
        save_response = save_voucher(voucher)
        if 'error' in save_response:
            raise Exception(save_response['error'])
        else:
            return build_response.build_json({
                "_id": str(save_response['voucher_id'])
            })
    except Exception as e:
        return build_response.build_json({"error": str(e)})



@vouchers.route('/<id>', methods=['DELETE'])
def delete_voucher(id):
    """
    Delete a voucher
    :param id:
    :return:
    """
    try:
        voucher = Voucher.objects.get(id=ObjectId(id))
    except Exception as e:
        return build_response.build_json({"error": str(e)})

    voucher.delete()
    return build_response.sent_ok()
