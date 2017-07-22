from lucky_club.database import db
from lucky_club.error_helper import InvalidUsage


def lot_edit(edited_lot, form_data):
    try:
        if 'name' not in form_data or not form_data['name'].strip():
            db.session.rollback()
            raise InvalidUsage('Field name is empty', status_code=400)
        name = form_data['name']
        edited_lot.name = name

        if 'description' not in form_data or not form_data['description'].strip():
            db.session.rollback()
            raise InvalidUsage('Field description is empty', status_code=400)
        description = form_data['description']
        edited_lot.description = description

        if 'full_description' not in form_data or not form_data['full_description'].strip():
            db.session.rollback()
            raise InvalidUsage('Field full_description is empty', status_code=400)
        full_description = form_data['full_description']
        edited_lot.full_description = full_description

        if 'category_id' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field category is empty', status_code=400)
        category = form_data['category_id']
        edited_lot.category_id = int(category)

        if 'count_participants' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field count_participants is empty', status_code=400)
        count_participants = form_data['count_participants']
        edited_lot.count_participants = int(count_participants)

        if 'price' not in form_data:
            db.session.rollback()
            raise InvalidUsage('Field price is empty', status_code=400)
        price = form_data['price']
        edited_lot.price = float(price)
    except:
        db.session.rollback()
        raise InvalidUsage('Wrong input data', status_code=400)

    return edited_lot
