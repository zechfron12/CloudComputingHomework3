from datetime import datetime
from flask import abort
from google.cloud import firestore

PROJECTID = 'cc-lab-3-382417'
db = firestore.Client(project=PROJECTID)
collection_name = 'appointments'


def routing(request):
    if request.method == 'POST':
        request_json = request.get_json()
        doc_ref = db.collection(collection_name).document()
        doc_ref.set(request_json)
        data = {}
        mandatory_keys = {
            'doctorId': False,
            'patientId': False,
            'startTime': False,
            'endTime': False
        }
        for key, value in request_json.items():
            if key in mandatory_keys:
                mandatory_keys[key] = True
            data[key] = value
        for key, value in mandatory_keys.items():
            if not value:
                abort(400, f'"{key}" is missing')
            value = str(data[key])
            if key == 'doctorId' or key == 'patientId':
                if not value.isalnum():
                    abort(400, f'"{key}" is not alphanumeric')
            if key == 'startTime' or key == 'endTime':
                try:
                    datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    abort(400, f'"{key}" is not a valid date')

        data = ','.join(f'"{key}": "{value}"' for key, value in data.items())
        res_json = '{'
        res_json += f'"id": "{doc_ref.id}",'
        res_json += data + '}'
        return res_json
    elif request.method == 'GET':
        res = ''
        docs = db.collection(collection_name).stream()
        for doc in docs:
            res += '{'
            data = doc.to_dict()
            data['id'] = doc.id
            res += ','.join(f'"{key}": "{value}"' for key, value in data.items())
            res += '},'
        res = res[:-1]
        res = '[' + res + ']'
        return res
    elif request.method == 'DELETE':
        request_json = request.get_json()
        doc_id = request_json.get('id')

        doc_id = str(doc_id)
        if not doc_id.isalnum():
            abort(400, 'id is not alphanumeric')

        doc = db.collection(collection_name).document(doc_id).get()
        if not doc.exists:
            abort(404, 'id does not exist')

        if doc_id is None:
            abort(400, 'id is missing')
        db.collection(collection_name).document(doc_id).delete()

        return f'Deleted document with id: {doc_id}'
    else:
        abort(405)

