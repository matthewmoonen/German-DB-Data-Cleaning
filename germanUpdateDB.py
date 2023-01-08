import sqlite3
from sqlite3 import Error

# ('Szenario', 'Szenarien')
# ('Lava', 'Laven')
# ('Teig', 'Teigrunder')
# ('Würze', 'Gewürze')
# ('Hinken', 'Hinkt')
# ('Kleiderschrank', 'Schränke')
# Modus, Modi
# Japaner, Japaneses
# Zummermann, zimmerleute
# elfenbeinarbeiten
# medikament, arzneimittel
# fernsehen, fernseher - is an error? No - https://www.reddit.com/r/German/comments/i1ux8p/der_fernseher_vs_das_fernsehen/
# Datum, daten
# level, niveaus

# xx. OTHER/ERROR

"""Unlike English, which mainly uses the suffix 's' to denote plural ('apple' -> 'apples', 'car' -> 'cars'), German plurals have a number of different rules. 
This script categorises nouns and their plurals into groups:

    1. no change
    2. add -e
    3. add -e + umlaut
    4. add -s
    5. add -er + umlaut
    6. add - n
    7. add - en
    8. add - n, (where the non-plural version ends with r)
    9. add - es
    10. add -er
    11. add - se
    12. add - le
    13. add - umlaut
"""

# 5 8


def main():
    
    database = "german.db"
    conn = create_connection(database)
    
    with conn:
        create_column(conn)
        get_plural_rule1(conn)
        get_plural_rule2(conn)
        get_plural_rules_7_9_10_11_12(conn)
        get_plural_rule_3(conn)
        get_null(conn)


def create_column(conn):
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE nouns_de ADD plural_rule TEXT")
    except:
        print('plural_rule column already exists. new column not created.')

def get_plural_rule_3(conn):
    umlaut_dictionary = {
        'a' : 'ä',
        'o' : 'ö',
        'u' : 'ü',
        'A' : 'Ä',
        'O' : 'Ö',
        'U' : 'Ü',
    }

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural) - 1")
    plural_rule_umlaut1 = cur.fetchall()

    for i in plural_rule_umlaut1:

        if i[0] == i[1][0:-1] and i[1][-1] == 'e':
            cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [2, i[0]])

        if i[0] == i[1][0:-1].replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U') and i[1][-1] == 'e':
            for index, value in enumerate(i[0]):
                if value in 'aouAOU' and i[1][index] == umlaut_dictionary[value]:
                    cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [3, i[0]])
                    continue
        
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural)")
    plural_rule_umlaut1 = cur.fetchall()

    for i in plural_rule_umlaut1:
        if i[0] == i[1].replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U'):
            for index, value in enumerate(i[0]):
                if value in 'aouAOU' and i[1][index] == umlaut_dictionary[value]:
                    cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [13, i[0]])
                    continue


def get_plural_rules_7_9_10_11_12(conn):
    """ Get all nouns whose plurals end in 'en', 'es', 'er', 'se' or 'le'
    """

    umlaut_dictionary = {
        'a' : 'ä',
        'o' : 'ö',
        'u' : 'ü',
        'A' : 'Ä',
        'O' : 'Ö',
        'U' : 'Ü',
    }

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = (LENGTH(plural) - 2)")

    plural_rule2 = cur.fetchall()


    for i in plural_rule2:

        if i[0] == i[1][0:-2]:
            if i[1][-2:] not in ['en', 'es', 'er', 'se', 'le']:
            elif i[1][-2:] == 'en': 
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [7, i[0]])
            elif i[1][-2:] == 'es':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [9, i[0]])
            elif i[1][-2:] == 'er':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [10, i[0]])
            elif i[1][-2:] == 'se':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [11, i[0]])
            elif i[1][-2:] == 'le':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [12, i[0]])

        elif i[0] == i[1][0:-2].replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U') and i[1][-2::] == 'er':
            for index, value in enumerate(i[0]):
                if value in 'aouAOU' and i[1][index] == umlaut_dictionary[value]:
                    cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [5, i[0]])
                    continue


def get_null(conn):
    """ Prints all nouns that haven't had a rule assigned. i.e. Null values.
    """

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE plural_rule IS NULL")
    plural_null = cur.fetchall()
    # for i in plural_null:
        # print(i)
    cur.execute("SELECT COUNT(noun) FROM nouns_de WHERE plural_rule IS NULL")
    print(cur.fetchone())

def get_plural_rule2(conn):

    """ Finds all nouns whose plural forms meet the following criteria:
            • the plural form is exactly one character longer than the singular form
            • the plural and non-plural forms are identical aside from the extra letter in the plural form
        
        Most 
    """

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural) - 1")

    plural_rule2 = cur.fetchall()
    for i in plural_rule2:

        if i[0] == i[1][0:-1]:

            if i[1][-1] not in 'sne':
                print(i[0] + " + " + i[1][-1] + ' = ' + i[1])
            elif i[1][-1] == 's':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [4, i[0]])
            elif i[1][-1] == 'n':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [6, i[0]])
            elif i[1][-1] == 'e':
                cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [6, i[0]])
                


def get_plural_rule1(conn):

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE noun=plural")
    plural_rule1 = cur.fetchall()
    for i in plural_rule1:
        cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [1, i[0]])


def create_connection(db_file):

    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    main()
























    # # Check that no nouns take more than one new umlaut in plural form:
    # for i in plural_rule_umlaut1:
    #     if i[1][-1] == 'e':
    #         for index, value in enumerate(i[0]):
    #             x = 0
    #             if value in 'aouAOU' and i[1][index] == umlaut_dictionary[value]:
    #                 x += 1
    #                 print(i)
    #             if x >= 2:
    #                 print(i)





# def get_plural_umlaut2(conn):
#     cur = conn.cursor()
#     cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural) - 2")

#     plural_rule_umlaut = cur.fetchall()

#     for i in plural_rule_umlaut():