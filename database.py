import sys
import os
import sqlite3
from contextlib import closing
from objects import Creature

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            print("Windows")
            DB_FILE = "creature.db"
        else:
            print("Linux")
            HOME = os.environ["HOME"]
            DB_FILE = "creature.db"
        
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row

def create_table():
    #is_player = 1 <- player
    #is_player = 0 <- creature
    with closing(conn.cursor()) as c:
        c.execute('DROP TABLE IF EXISTS creatures')
        c.execute(''' CREATE TABLE IF NOT EXISTS creatures (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            initiative INTEGER NOT NULL,
            health INTEGER NOT NULL,
            armorClass INTEGER NOT NULL,
            is_player BOOLEAN NOT NULL
        )
        ''')
        conn.commit()

def add_into_order(creature):
    with closing(conn.cursor()) as c:
        c.execute('''INSERT INTO creatures (id, name, initiative, health, armorClass, is_player) VALUES (?,?,?,?,?,?)''',
                  (creature.id, creature.name, creature.initiative, creature.health, creature.armorClass, creature.is_player))
        conn.commit()


def update_value(id, health, ac):
    with closing(conn.cursor()) as c:
        c.execute('UPDATE creatures SET health = ?, armorClass = ? WHERE id = ?', (health, ac, id))
        conn.commit()

def remove_selected_item(id):
    with closing(conn.cursor()) as c:
        c.execute('''DELETE FROM creatures WHERE id = ?''', (id,))
        conn.commit()

def clear_creatures():
    with closing(conn.cursor()) as c:
        c.execute('DELETE FROM creatures WHERE is_player = 0')
        conn.commit()

def clear_players():
    with closing(conn.cursor()) as c:
        c.execute('DELETE FROM creatures WHERE is_player = 1')
        conn.commit()

def clear_table():
    with closing(conn.cursor()) as c:
        c.execute('''SELECT * FROM creatures''')
        c.execute('''DELETE FROM creatures''')
        conn.commit()

def get_all_creatures():
    with closing(conn.cursor()) as c:
        c.execute('''SELECT * FROM creatures ORDER BY initiative DESC''')
        return c.fetchall()