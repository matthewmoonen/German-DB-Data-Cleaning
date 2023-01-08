import sqlite3
from sqlite3 import Error




def main():
    
    database = "german.db"
    conn = create_connection(database)
    


    with conn:
        quarantine_duplicates(conn)



def quarantine_duplicates(conn):

    """ 
    Compares the similarity of nouns to their duplicate forms where duplicate nouns exist in the database, AND the entries for the plural forms are different.
    Assigns 'points' of similarity between the duplicates and eliminates the plural with the least similarity.
    
    For example: the noun 'apple' may have two entries. In one entry, the plural is listed as 'apples', in the another plural is listed as 'fruits'.
    In this case, 'fruits' would be eliminated as it is less similar to 'apple' than 'apples'

    
    """

    cur = conn.cursor()
    cur.execute("SELECT id, noun, plural FROM nouns_de")
    all_nouns = cur.fetchall()
    
    
   





def get_plural_umlaut1(conn):
    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural) - 1")

    plural_rule_umlaut1 = cur.fetchall()


    umlaut_dictionary = {
        'a' : 'ä',
        'o' : 'ö',
        'u' : 'ü',
        'A' : 'Ä',
        'O' : 'Ö',
        'U' : 'Ü',
    }




    for i in plural_rule_umlaut1:
        if i[0] == i[1][0:-1].replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U') and i[1][-1] == 'e':
            for index, value in enumerate(i[0]):
                if value in 'aouAOU' and i[1][index] == umlaut_dictionary[value]:
                    cur.execute("UPDATE nouns_de SET plural_rule = ? WHERE noun = ?", [3, i[0]])
                    continue






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



def get_plural_rule7(conn):
    """ Get all nouns whose plurals end in 'en' or 'es'
    """

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE LENGTH(noun) = LENGTH(plural) - 2")

    plural_rule2 = cur.fetchall()

    for i in plural_rule2:

        if i[0] == i[1][0:-2]:
            # print(i)
            if i[1][-2:] not in ['en', 'es', 'er', 'se', 'le']:
                print(i)
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




# 7. add - en
# 9. add - es
# 10. add -er
# 11. add - se
# 12. add - le












    # for i in plural_null:
    #     print(i[1][-2])
    #     # if i[1][-2::] not in ['en', 'es']:
    #     #         print(i[0] + " + " + i[1][-2] + ' = ' + i[1])



def get_null(conn):
    """ Prints all nouns that haven't had a rule assigned. i.e. Null values.
    """

    cur = conn.cursor()
    cur.execute("SELECT noun, plural FROM nouns_de WHERE plural_rule IS NULL")
    plural_null = cur.fetchall()
    for i in plural_null:
        print(i)

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