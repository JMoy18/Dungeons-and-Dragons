from flask import Flask, jsonify, request, render_template, request, redirect, url_for

app = Flask(__name__)

class Creature:
    def __init__(self, name, initiative, health, armorClass, quantity = 1, is_player=False,):
        self.name = name
        self.initiative = initiative
        self.is_player = is_player
        self.health = health
        self.quantity = quantity
        self.armorClass = armorClass

creatures = []
players = []

@app.route('/')
def index():
    #this sorts the creatures in 
    all_characters = sorted(creatures + players, key=lambda x: int(x.initiative), reverse=True)
    return render_template('index.html', characters=all_characters)

@app.route('/add_creature', methods=['POST'])
def add_creature():
    name = request.form.get('name')
    initiative = request.form.get('initiative')
    health = request.form.get('health')
    armorClass = request.form.get("armorClass")
    quantity = request.form.get("quantity")
    is_player = request.form.get('is_player') == 'on'  # Checkbox value

    try:
        initiative = int(initiative)
        health = int(health)
        armorClass = int(armorClass)
    except ValueError:
        # Validation failed, render the template with a warning message
        return render_template('index.html', characters=creatures + players, warning_message='Initiative/Health/AC must be a valid number')
    
    if quantity == '':
        quantity = "1"

    numCreatures = int(quantity)

    while numCreatures != 0:
        if is_player:
            player = Creature(name, initiative, health, armorClass, is_player=True)
            players.append(player)
            numCreatures -= 1
        else:
            creature = Creature(name, initiative, health, armorClass)
            creatures.append(creature)
            numCreatures -= 1

    return redirect(url_for('index'))

@app.route('/update_character', methods=['POST'])
def update_character():
    name = request.form.get('name')
    property_name = request.form.get('property')
    value = request.form.get('value')

    #something is broken here, in the case of multiple of the same name, we want to know which index it is at
    for character in creatures + players:
        if character.name == name:
            setattr(character, property_name, value)

    return jsonify({'success': True})

@app.route('/remove_selected', methods=['POST'])
def remove_selected():
    selected_info = request.form.get('selected_info')

    # Extract the character information from the selected_info
    selected_info_parts = selected_info.split(' - ')
    initiative = int(selected_info_parts[0].split(': ')[1])
    name = selected_info_parts[1].split(': ')[1]
    health = int(selected_info_parts[2].split(': ')[1])
    armor_class = int(selected_info_parts[3].split(': ')[1])
    is_player = selected_info_parts[4].split(': ')[1] == 'Yes'

    #something is breaking if all is similar but AC, it does delete an item but it reverts the change back to the original value
    # Remove the character
    for character in creatures + players:
        if character.initiative == initiative and character.name == name and character.health == health and character.armorClass == armor_class and character.is_player == is_player:
            if character in creatures:
                creatures.remove(character)
            elif character in players:
                players.remove(character)

            #we only want to delete one item (case where two creatures have the same amount of health left and name, AC)
            break   

    return redirect(url_for('index'))


@app.route('/remove_creatures', methods=['POST'])
def remove_creatures():
    creatures.clear()
    return redirect(url_for('index'))

@app.route('/remove_players', methods=['POST'])
def remove_players():
    players.clear()
    return redirect(url_for('index'))

@app.route('/remove_all', methods=['POST'])
def remove_all():
    creatures.clear()
    players.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

