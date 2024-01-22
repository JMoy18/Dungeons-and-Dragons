from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Creature:
    def __init__(self, name, initiative, health, armorClass, is_player=False,):
        self.name = name
        self.initiative = initiative
        self.is_player = is_player
        self.health = health
        self.armorClass = armorClass

creatures = []
players = []

@app.route('/')
def index():
    all_characters = sorted(creatures + players, key=lambda x: int(x.initiative), reverse=True)
    return render_template('index.html', characters=all_characters)

@app.route('/add_creature', methods=['POST'])
def add_creature():
    name = request.form.get('name')
    initiative = request.form.get('initiative')
    health = request.form.get('health')
    armorClass = request.form.get("armorClass")
    is_player = request.form.get('is_player') == 'on'  # Checkbox value

    try:
        initiative = int(initiative)
        health = int(health)
        armorClass = int(armorClass)
    except ValueError:
        # Validation failed, render the template with a warning message
        return render_template('index.html', characters=creatures + players, warning_message='Initiative/Health/AC must be a valid number')

    if is_player:
        player = Creature(name, initiative, health, armorClass, is_player=True)
        players.append(player)
    else:
        creature = Creature(name, initiative, health, armorClass)
        creatures.append(creature)

    return redirect(url_for('index'))

@app.route('/remove_selected', methods=['POST'])
def remove_selected():
    selected_info = request.form.get('selected_info')

    # Example: Remove the item with the matching name, initiative, and player status
    for character in creatures + players:
        if f"{character.name} - Initiative: {character.initiative} - Player: {character.is_player}" == selected_info:
            if character in creatures:
                creatures.remove(character)
            elif character in players:
                players.remove(character)

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

