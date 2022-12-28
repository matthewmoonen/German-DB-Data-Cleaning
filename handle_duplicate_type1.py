import sqlite3
from sqlite3 import Error



def main():
    
    database = "german.db"
    conn = create_connection(database)

    with conn:
        get_duplicates_with_repeated_plural_forms(conn)



def get_duplicates_with_repeated_plural_forms(conn):

    """Find nouns that have a duplicate
        Classify the type of duplicate
        Handle duplicates of a certain kind (where the English translation is different but all else identical)
    """


    # Select all nouns as a list of tuples
    cur = conn.cursor()
    cur.execute("SELECT noun FROM nouns_de")
    all_nouns = cur.fetchall()

    # Iterate over list, find number of instances of each noun in the DB
    for i in all_nouns:
        cur.execute("SELECT COUNT(noun) FROM nouns_de WHERE noun=?", i)
        count_of_i = cur.fetchone()

        # If noun is repeated, get its plural and id
        if count_of_i[0] > 1:
            cur.execute("SELECT plural FROM nouns_de WHERE noun=?", i)
            all_i = cur.fetchall()
            plural_list = []
            for j in all_i:
                plural_list.append(j[0])

            # Check whether plural form is ALSO identical. I.e. it is an identical duplicate entry with two or more English translations
            repeated_plural = ''
            while len(plural_list) > 1:
                x = plural_list.pop()
                if x in plural_list:
                    repeated_plural = x
                    break
            if repeated_plural == '':
                continue
            

            # Combine duplicate entries, where two different English translations exist, into a single row. 
            else:
                cur.execute("SELECT id, noun, plural, english FROM nouns_de WHERE noun=? AND plural=?", [i[0], repeated_plural])
                all_instances_of_repeated_noun_and_plural = cur.fetchall()

                # Dynamically expand the number of columns in the table as needed.
                entry_to_add_extra_translations_to = all_instances_of_repeated_noun_and_plural.pop(0)
                
                # Check whether more two or more English translations already exist. If so, avoid overwriting existing entries.
                english_column = 2
                while True:
                    english_column_string = 'english' + str(english_column)
                    query = 'SELECT ' + english_column_string + 'FROM nouns_de WHERE id=' + str(entry_to_add_extra_translations_to[0])
                    try:

                        """
                        --- WARNING --- Don't use this next line in a production environment. It is a security risk. See README.md
                        """
                        cur.execute(query)
                        """ 
                        / --- WARNING ---
                        """

                    except sqlite3.OperationalError:
                        break
                    if cur.fetchone()[0] != None:
                        english_column += 1
                        continue
                    else:
                        break


                for k in all_instances_of_repeated_noun_and_plural:
                    english_column_string = 'english' + str(english_column)
                    
                    query = "update nouns_de SET " + english_column_string + "=\"" + k[3] + "\" WHERE id=" + str(entry_to_add_extra_translations_to[0])
                    try:
            

                        """
                        --- WARNING --- Don't use this next line in a production environment. It is a security risk. See README.md
                        """
                        cur.execute(query)
                        """ 
                        / --- WARNING ---
                        """


                    except sqlite3.OperationalError:

                        query1 = "ALTER TABLE nouns_de ADD english" + str(english_column) + " TEXT"

                        """
                        --- WARNING --- Don't use the next two lines in a production environment. It is a security risk. See README.md
                        """
                        cur.execute(query1)
                        cur.execute(query)
                        """ 
                        / --- WARNING ---
                        """

                        english_column += 1
                    finally:
                        query = "DELETE FROM nouns_de WHERE id=" + str(k[0])
                        cur.execute(query)
                        english_column += 1



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