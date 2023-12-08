import time
import mysql.connector as mcon
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
username=input("please enter your username:")
password=input("please enter hyour password")

my_con = mcon.connect(
            host='localhost',
            user='root',
            password='',
            database='hospital')
mysql = my_con.cursor()

if my_con:
    mysql = my_con.cursor()
    mysql.execute("SELECT catagory FROM data WHERE email = %s AND passwords= %s", (username, password,))
    cat = mysql.fetchone()

    if cat and cat[0] == "admin":
        ##loading()
        while True:
            print("\nMenu:")
            print("1. View data in a table")
            print("2. Update data")
            print("3. Delete data")
            print("4. Create a new table")
            print("5. Delete a table")
            print("6. Alter a table")
            print("7. Search for wildcard character")
            print("8. Graphs")
            print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")


                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")

                mysql.execute(f"SHOW COLUMNS FROM {tbname}")
                columns = mysql.fetchall()

                print(f"Columns in {tbname}:")
                for i, column in enumerate(columns, start=1):
                    print(f"{i}. {column[0]}")
                clminp = input("Enter the names of the columns you want (comma-separated): ")
                if clminp=="":
                    clminp="*"
                condition = input("Enter the condition (e.g., 'column_name = value'): ")
                order_direction = input("Enter 'ASC' for ascending or 'DESC' for descending: ")
                order_direction = order_direction.upper()
                ordcl= columns[0]
                ordcl=ordcl[0]

                if order_direction not in ["ASC", "DESC"]:
                    order_direction = "ASC"

                if condition == "" and clminp == "":
                    sql_query = "SELECT * FROM " + tbname + " ORDER BY "+ordcl +" "+ order_direction + ";"
                elif condition == "":
                    sql_query = "SELECT " + clminp + " FROM " + tbname + " ORDER BY "+ordcl +" "+ order_direction + ";"
                elif clminp == "":
                    sql_query = "SELECT * FROM " + tbname + " WHERE " + condition + " ORDER BY "+ordcl +" "+ order_direction + ";"
                else:
                    sql_query = "SELECT " + clminp + " FROM " + tbname + " WHERE " + condition + " ORDER BY "+ordcl +" "+ or-der_direction + ";"

                print(sql_query)

                try:
                    mysql.execute(sql_query)
                    result = mysql.fetchall()

                    if result:
                        print("Selected Data:")
                        for row in result:
                            print(row)
                    else:
                        print("No data matching the condition.")
                except mcon.Error as err:
                    print(f"Error executing SELECT query: {err}")



            elif choice == '2':
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")

                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")
                condition = input("Enter the condition (e.g., 'column_name = value'): ")
                new_data = input("Enter the new data (e.g., 'column_name = new_value'): ")

                # Construct the SQL query
                sql_query = "UPDATE "+ tbname +" SET "+ new_data +" WHERE "+ condition +";"

                try:
                    mysql.execute(sql_query)
                    mysql.connection.commit()
                    print("Data updated successfully.")

                except mcon.Error as err:
                    print(f"Error updating data: {err}")

            elif choice == '3':
                ##loading()
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")

                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")
                condition = input("Enter the condition (e.g., 'column_name = value'): ")
                sql_query = "DELETE FROM "+tbname+" WHERE "+condition+";"

                try:
                    mysql.execute(sql_query)
                    mysql.connection.commit()
                    print("Data deleted successfully.")

                except mcon.Error as err:
                    print(f"Error deleting data: {err}")

            elif choice == '4':

                tbname = input("Enter the name of the new table: ")
                num_columns = int(input("Enter the number of columns: "))

                columns = []
                for i in range(num_columns):
                    column_name = input(f"Enter name for column {i + 1}: ")
                    column_type = input(f"Enter data type for column {i + 1}: ")
                    columns.append(f"{column_name} {col-umn_type}")

                # Construct the SQL query
                sql_query = f"CREATE TABLE {tbname} ({', '.join(columns)});"

                try:
                    mysql.execute(sql_query)
                    print(f"Table '{tbname}' created success-fully.")

                except mcon.Error as err:
                    print(f"Error creating table: {err}")
            elif choice == '5':
                table_name = input("Enter the name of the table to delete: ")

                # Construct the SQL query
                sql_query = f"DROP TABLE {table_name};"

                try:
                    mysql.execute(sql_query)
                    print(f"Table '{table_name}' deleted successfully.")

                except mcon.Error as err:
                    print(f"Error deleting table: {err}")

            elif choice == '6':
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")

                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")

                print("Available options for altering the ta-ble:")
                print("1. edit column")
                print("2. Delete column")
                option = input("Enter your choice: ")

                if option == '1':
                    column_name = input("Enter the name of the new column: ")
                    column_type = input("Enter data type for the new column: ")

                    # Construct the SQL query
                    sql_query = f"ALTER TABLE {tbname} ADD COLUMN {column_name} {column_type};"

                elif option == '2':
                    mysql.execute(f"SHOW COLUMNS FROM {tbname}")
                    columns = mysql.fetchall()
                    print(columns)
                    old_column_name = input("Enter the name of the column to modify: ")
                    new_column_name = input("Enter the new name for the column: ")
                    new_column_type = input("Enter the new data type for the column: ")

                    # Construct the SQL query
                    sql_query = f"ALTER TABLE {tbname} CHANGE COLUMN {old_column_name} {new_column_name} {new_column_type};"

                elif option == '3':
                    column_name = input("Enter the name of the column to delete: ")

                    # Construct the SQL query
                    sql_query = f"ALTER TABLE {tbname} DROP COLUMN {column_name};"

                else:
                    print("Invalid option.")


                try:
                    mysql.execute(sql_query)
                    print(f"Table '{tbname}' altered success-fully.")

                except mcon.Error as err:
                    print(f"Error altering table: {err}")


            elif choice == '7':
                wildcard = input("Enter the character you want to search for: ")
                mysql.execute("SHOW TABLES")
                tables = [table[0] for table in mysql.fetchall()]

                for tbname in tables:
                    # Get a list of all columns in the table.
                    mysql.execute(f"SHOW COLUMNS FROM {tbname}")
                    columns = [column[0] for column in mysql.fetchall()]

                    for column in columns:
                        # Construct and execute a query to search for the wildcard character in the column.
                        query = f"SELECT * FROM {tbname} WHERE {column} LIKE %s"
                        params = (f"%{wildcard}%",)  # Add '%' before and after the wildcard character.

                        mysql.execute(query, params)
                        results = mysql.fetchall()

                        if results:
                            print(f"Table: {tbname}, Column: {column}")
                            print("Matching Rows:")
                            for row in results:
                                print(row)
            elif choice=='8':

                print("Possible graphs:"
                      "1. Comparison of prices of medicines"
                      "2. Observed diseases"
                      "3. Exit")
                choice = int(input("Enter your choice (1/2/3): "))

                if choice == 1:
                    mysql.execute("SELECT NAME, Price FROM medication_prices")
                    data = mysql.fetchall()
                    if data:
                        df = pd.DataFrame(data, col-umns=["Medication", "Price"])
                        df.plot.bar(x="Medication", y="Price", title="Comparison of Medication Prices")
                        plt.show()
                    else:
                        print("No data found for medication prices.")

                elif choice == 2:
                    while True:
                        lst = []
                        mysql.execute("select diseases from pa-tients")
                        y = mysql.fetchall()
                        df = pd.DataFrame({"": y})
                        df.columns = ["diseases"]
                        print(df)
                        x = 0
                        while len(df) != x:
                            y = df.iloc[x, 0]
                            input_tuple = y
                            # Extract the string from the tuple
                            input_str = input_tuple[0]

                            # Split the string into a list of substrings using ',' as the delimiter
                            integers_as_strings = in-put_str.split(',')

                            # Convert each substring to an integer and print it
                            for num_str in integers_as_strings:
                                lst.append(int(num_str))
                            x += 1
                        df = pd.DataFrame({"dis": lst})

                        df = df['dis'].value_counts().reset_index()
                        mysql.execute("SELECT scientific_name FROM disease LIMIT 10;")
                        namedis = mysql.fetchall()
                        # Step 8: Plot the disease names and their counts
                        print(df)
                        plt.bar(df['dis'], df['count'])
                        plt.ylim(300)

                        # Show the plot
                        plt.show()
                elif choice == 3:
                    pass
                else:
                    print("it appears the data you entered is wrong,kindly re-enter it")
            elif choice == '9':
                my_con.close()
                print("Exiting the program.")
                break
            else:
                print("it appears the data you entered is wrong,kindly re-enter it")


    elif cat and cat[0] == "doctors":
        while True:
            print("\nMenu:")
            print("1. View data in a table")
            print("2. Update data")
            print("3. Exit")

            choice = int(input("Enter your choice: "))

            if choice == '1':
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")

                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")

                mysql.execute(f"SHOW COLUMNS FROM {tbname}")
                columns = mysql.fetchall()

                print(f"Columns in {tbname}:")
                for i, column in enumerate(columns, start=1):
                    print(f"{i}. {column[0]}")
                clminp = input("Enter the names of the columns you want (comma-separated): ")
                if clminp == "":
                    clminp = "*"
                condition = input("Enter the condition (e.g., 'column_name = value'): ")
                order_direction = input("Enter 'ASC' for ascending or 'DESC' for descending: ")
                order_direction = order_direction.upper()
                if order_direction not in ["ASC", "DESC"]:
                    order_direction = "ASC"
                if condition == "" and clminp == "":
                    sql_query = "SELECT * FROM " + tbname + " ORDER BY " + order_direction + ";"
                elif condition == "":
                    sql_query = "SELECT " + clminp + " FROM " + tbname + "+ ORDER BY " + order_direction + ";"
                elif clminp == "":
                    sql_query = "SELECT * FROM " + tbname + "WHERE" + condition + " ORDER BY " + order_direction + ";"
                else:
                    sql_query = "SELECT " + clminp + " FROM " + tbname + " WHERE " + condition + " ORDER BY " + order_direction + ";"
                print(sql_query)

                try:
                    mysql.execute(sql_query)
                    result = mysql.fetchall()

                    if result:
                        print("Selected Data:")
                        for row in result:
                            print(row)
                    else:
                        print("No data matching the condition.")

                except mcon.Error as err:
                    print(f"Error executing SELECT query: {err}")


            elif choice == '2':
                mysql.execute("SHOW TABLES")
                tables = mysql.fetchall()

                print("Available Tables:")
                for i, table in enumerate(tables, start=1):
                    print(f"{i}. {table[0]}")

                table_choice = int(input("Select a table (enter the number): "))
                if 1 <= table_choice <= len(tables):
                    tbname = tables[table_choice - 1][0]
                else:
                    print("Invalid choice. Please select a valid table.")
                condition = input("Enter the condition (e.g., 'column_name = value'): ")
                new_data = input("Enter the new data (e.g., 'column_name = new_value'): ")

                # Construct the SQL query
                sql_query = "UPDATE " + tbname + " SET " + new_data + " WHERE " + condition + ";"

                try:
                    mysql.execute(sql_query)
                    mysql.connection.commit()
                    print("Data updated successfully.")

                except mcon.Error as err:
                    print(f"Error updating data: {err}")

            elif choice == '3':
                my_con.close()
                print("Exiting the program.")
                break
            else:
                print("it appears the data you entered is wrong,kindly re-enter it")

    elif cat and cat[0] == "user":
        while True:
            print("\nMenu:")
            print("1.view personal data")
            print("2.view diseases encountered by now")
            print("3.purchase medicines")
            print("4.exit")

            choice = int(input("Enter your choice: "))
            if choice == 1:

                try:
                    sql = "SELECT * FROM patients WHERE email = %s"
                    params = (username,)
                    mysql.execute(sql, params)
                    result = mysql.fetchall()

                    if result:
                        print("Selected Data:")
                        for row in result:
                            print(row)
                    else:
                        print("No data matching the condition.")

                except mcon.Error as err:
                    print(f"Error executing SELECT query: {err}")



            if choice == 2:
                ##loading()
                mysql.execute("SELECT diseases FROM patients WHERE email = %s", (username,))

                # Fetch the results
                myresult = mysql.fetchall()

                # Print the diagnosed diseases and recommended medicines
                print("You have been diagnosed with the following diseases (with the names of recommended medicines):")
                for row in myresult:
                    diseases = row[0].split(",")  # Split dis-eases if they are comma-separated
                    for disease in diseases:
                        disease = disease.strip()  # Remove leading/trailing spaces (like trim)
                        disease_id = f"d_{disease.replace(' ', '_')}"  # Create the disease ID
                        disease_id = disease_id.replace(",", "")  # Remove commas from disease ID
                        # Execute a query to fetch details of the disease and recommended medicines
                        mysql.execute("SELECT * FROM disease WHERE disease_id = %s", (disease_id,))
                        disease_info = mysql.fetchall()

                        # Print disease information
                        if disease_info:
                            print(
                                f"Disease: {disease_info[0][1]}")  # f for strings and [0][1]Means first row 3rd coloumn
                            print(
                                f"Recommended Medicines: {dis-ease_info[0][2], disease_info[0][3], disease_info[0][4]}")
                            print()


            if choice == 3:
                print("Available medicines:")
                mysql.execute("SELECT * FROM medication_prices")
                med = mysql.fetchall()
                for item in med:
                    print(f"ID: {item[3]}, Name: {item[0]}, Price: ${item[1]}, Quantity: {item[2]}")
                mysql.execute("SELECT user_id FROM patients WHERE email = %s", (username,))
                userid = mysql.fetchall()
                userid= userid[0]
                userid = userid[0]
                item_id = int(input("Enter the ID of the med you want to buy: "))
                quantity = int(input("Enter the quantity you want to buy: "))
                dt = datetime.datetime.now()
                mysql.execute("SELECT name, price, qty FROM medication_prices WHERE med_id = %s", (item_id,))
                item = mysql.fetchone()


                if item:
                    item_name, item_price, item_quantity = item
                    if item_quantity >= quantity:
                        total_cost = item_price * quantity
                        print(f"Item: {item_name}, Quantity: {quantity}, Total Cost: ${total_cost}")

                        confirm = input("Confirm purchase (yes/no): ").strip().lower()
                        if confirm == "yes":
                            # Deduct the purchased quantity from the item's quantity
                            mysql.execute("UPDATE medica-tion_prices SET qty = qty - %s WHERE med_id = %s",(quantity, item_id))
                            print(userid, dt, item_id, quantity)

                            sql = "INSERT INTO med_purchased (uid, date, med_id, qty_pur) VALUES (%s, %s, %s, %s)"


                            params = (userid, dt, item_id, quantity)


                            mysql.execute(sql, params)
                            print("Purchase successful!")
                        else:
                            print("Purchase canceled.")
                    else:
                        print("Insufficient quantity available.")
                else:
                    print("Item not found.")

            elif choice == 4:
                pass
            else:
                print("it appears the data you entered is wrong,kindly re-enter it")

    else:
        print("It seems that an unexpected error has occurred. Please inform the staff about it.")


