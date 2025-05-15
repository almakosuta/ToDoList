
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

#  definierte Listen mit UUIDs
todo_lists = [
    {'id': 'f1001abc-0001-4bfa-8123-a1f0cde12345', 'name': 'Einkaufsliste'},
    {'id': 'f1002abc-0002-4bfa-8123-a1f0cde12345', 'name': 'Arbeit'},
    {'id': 'f1003abc-0003-4bfa-8123-a1f0cde12345', 'name': 'Reisen'},
    {'id': 'f1004abc-0004-4bfa-8123-a1f0cde12345', 'name': 'Fitness'},
]

# Aufgaben zu den Listen mit dynamisch generierten IDs
todos = [
    # Einkaufsliste
    {'id': str(uuid.uuid4()), 'name': 'Milch kaufen', 'description': '1L Vollmilch', 'list': 'f1001abc-0001-4bfa-8123-a1f0cde12345'},
    {'id': str(uuid.uuid4()), 'name': 'Eier holen', 'description': '6 Bio-Eier', 'list': 'f1001abc-0001-4bfa-8123-a1f0cde12345'},

    # Arbeit
    {'id': str(uuid.uuid4()), 'name': 'Meeting vorbereiten', 'description': 'Folien für Quartalspräsentation erstellen', 'list': 'f1002abc-0002-4bfa-8123-a1f0cde12345'},
    {'id': str(uuid.uuid4()), 'name': 'Code Review', 'description': 'Backend-Pull-Requests prüfen', 'list': 'f1002abc-0002-4bfa-8123-a1f0cde12345'},

    # Reisen
    {'id': str(uuid.uuid4()), 'name': 'Hotel buchen', 'description': '3 Nächte in Berlin reservieren', 'list': 'f1003abc-0003-4bfa-8123-a1f0cde12345'},
    {'id': str(uuid.uuid4()), 'name': 'Koffer packen', 'description': 'Wetterfeste Kleidung einpacken', 'list': 'f1003abc-0003-4bfa-8123-a1f0cde12345'},

    # Fitness
    {'id': str(uuid.uuid4()), 'name': 'Joggen gehen', 'description': '5km Lauf im Park', 'list': 'f1004abc-0004-4bfa-8123-a1f0cde12345'},
    {'id': str(uuid.uuid4()), 'name': 'Fitnessstudio', 'description': 'Beine und Rücken trainieren', 'list': 'f1004abc-0004-4bfa-8123-a1f0cde12345'},
]

@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# hilfsfunktionen
def find_list(list_id):
    return next((l for l in todo_lists if l['id'] == list_id), None)

def find_entry(list_id, entry_id):
    return next((e for e in todos if e['list'] == list_id and str(e['id']) == entry_id), None)

# GET alle Listen
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

# POST neue Liste
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    data = request.get_json(force=True)
    if 'name' not in data:
        abort(400)
    new_list = {'id': str(uuid.uuid4()), 'name': data['name']}
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# GET einzelne Liste
@app.route('/todo-list/<list_id>', methods=['GET'])
def get_list(list_id):
    list_item = find_list(list_id)
    if not list_item:
        abort(404)
    return jsonify(list_item), 200

# DELETE komplette Liste
@app.route('/todo-list/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    list_item = find_list(list_id)
    if not list_item:
        abort(404)
    todo_lists.remove(list_item)
    global todos
    todos = [t for t in todos if t['list'] != list_id]
    return jsonify({'msg': 'success'}), 200

# GET alle Einträge einer Liste
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_entries(list_id):
    if not find_list(list_id):
        abort(404)
    return jsonify([e for e in todos if e['list'] == list_id]), 200

# POST neuen Eintrag
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if not find_list(list_id):
        abort(404)
    data = request.get_json(force=True)
    if 'name' not in data or 'description' not in data:
        abort(400)
    new_entry = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'description': data['description'],
        'list': list_id
    }
    todos.append(new_entry)
    return jsonify(new_entry), 200

# PUT Eintrag aktualisieren
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    if not find_list(list_id):
        abort(404)
    entry = find_entry(list_id, entry_id)
    if not entry:
        abort(404)
    data = request.get_json(force=True)
    if 'name' not in data or 'description' not in data:
        abort(400)
    entry['name'] = data['name']
    entry['description'] = data['description']
    return jsonify(entry), 200

# DELETE Eintrag löschen
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if not find_list(list_id):
        abort(404)
    entry = find_entry(list_id, entry_id)
    if not entry:
        abort(404)
    todos.remove(entry)
    return jsonify({'msg': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)