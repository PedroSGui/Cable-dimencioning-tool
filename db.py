
import sqlite3

from sqlite3 import Error


def create_connection(path):

    connection = None

    try:

        connection = sqlite3.connect(path)

        print("Connection to SQLite DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")


    return connection

connection = create_connection(".\sm_app.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_users_table = """
CREATE TABLE IF NOT EXISTS cabos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  material INTEGER NOT NULL,
  section INTEGER NOT NULL,
  perfil INTEGER NOT NULL,
  conductors INTEGER NOT NULL
);
"""
execute_query(connection, create_users_table)  



create_users = """
INSERT INTO
  cabos (material, section, perfil, conductors)
VALUES
  (0, 40, 1, 1),
  (1, 45, 2, 3);
"""

execute_query(connection, create_users)





def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



'''
for cabos in cabos:
    print(cabos)
'''



# Começa a partir daqui


menu_options = {
    1: 'Adicionar itens',
    2: 'Ver tabela',
    3: 'Calculo de secção',
    4: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    material = input('Qual o material (0 pra cobre e 1 pra aluminio): ')
    section = input('Qual a secção: ')
    perfil = input('Qual o perfil: ')
    conductors = input('Quantos condutores: ')
    cabo_a_adicionar = "(" + material + ", " + section + ", "+ perfil + ", "+conductors + ")"
    create_users = "INSERT INTO cabos (material, section, perfil, conductors) VALUES " + cabo_a_adicionar
    print(cabo_a_adicionar)
    execute_query(connection, create_users)

def option2():
    select_cabos = "SELECT * from cabos"
    cabos = execute_read_query(connection, select_cabos)
    print("\n\n")
    for cabos in cabos:
        print(cabos)
    print("\n\n")

def option3():
    f=1


if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


# Não escreve daqui pra baixo