from flask import Flask, jsonify, request, jsonify, render_template, request, redirect, url_for
import database
from objects import Creature
app = Flask(__name__)
id_number = 1

@app.route('/')
def index():
    creatures = database.get_all_creatures()
    return render_template('index.html', creatures=creatures)

@app.route('/add_creature', methods=['POST'])
def add_creature():
    global id_number
    data = request.get_json()
    name = data.get('name')
    initiative = data.get('initiative')
    health = data.get('health')
    armorClass = data.get("armorClass")
    quantity = data.get("quantity")
    is_player = data.get('is_player')

    if not quantity:
        quantity = 1

    try:
        initiative = int(initiative)
        health = int(health)
        armorClass = int(armorClass)
        quantity = int(quantity)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid input type'})

    for _ in range(quantity):
        creature = Creature(name = name, id = id_number, initiative = initiative, health = health, armorClass= armorClass, is_player=is_player)
        id_number += 1
        database.add_into_order(creature)

    return jsonify({'success': True})

@app.route('/update_character', methods=['PUT'])
def update_character():
    data = request.get_json()
    id = data.get('data-id')
    name = data.get('name')
    initiative = data.get('initiative')
    health = data.get('health')
    armorClass = data.get('armorClass')
    is_player = data.get('is_player')

    database.update_value(id, (name, initiative, health, armorClass, is_player))
    return jsonify({'success': True})

@app.route('/remove_selected', methods=['DELETE'])
def remove_selected():
    data = request.get_json()
    creature_id = data.get('id')
    if creature_id is not None:
        database.remove_selected_item(creature_id)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'ID not provided'})


@app.route('/remove_creatures', methods=['POST'])
def remove_creatures():
    database.clear_creatures()
    return redirect(url_for('index'))

@app.route('/remove_players', methods=['POST'])
def remove_players():
    database.clear_players()
    return redirect(url_for('index'))

@app.route('/remove_all', methods=['POST'])
def remove_all():
    database.clear_table()
    return redirect(url_for('index'))

def main():
    database.connect()
    database.create_table()
    app.run(debug=True)


if __name__ == '__main__':
    main()


