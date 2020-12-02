import mysql.connector
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

# If you are using this on your system, please make sure to change the user and password values to your mysql server's appropriate username and password.
mydb = mysql.connector.connect(
    host="localhost", user="shreyas", password="root", database="passwordmanager"
)
cursor = mydb.cursor()
masterU = ""
sql = "CREATE TABLE IF NOT EXISTS users(username varchar(100), password varchar(100));"
cursor.execute(sql)
mydb.commit()
while True:
    print("\n\n\n" + "-" * 90)
    print(("-" * 13) + "Welcome to the Password Manager" + ("-" * 13))
    print(
        "You will need to login with your username and master password to access other passwords.(yeah its ironic but safety first :))\n"
    )
    user = int(input("1: New user \n2: Existing user \n\n~ "))
    print("-" * 90)
    if user == 1:
        while True:
            username = input(
                "Please enter a username you want to use for this program\n~ "
            )
            password = input("Please enter the master password for this program\n~ ")
            confirm = input("Please re enter your password for confirmation\n~ ")
            if password == confirm:
                sql = "INSERT INTO users VALUES(%s,%s);"
                val = (username, password)
                cursor.execute(sql, val)
                mydb.commit()
                print("User Successfully created. You can now login\n\n")
                sql1 = (
                    "CREATE TABLE "
                    + username
                    + "(platform varchar(500),username varchar(500),password varchar(2000),crypt varchar(2000));"
                )
                cursor.execute(sql1)
                mydb.commit()
                break
            else:
                print("Mismatch in passwords. Please enter again\n\n")
    elif user == 2:
        f = 0
        while True:
            username = input("Please enter your username for this account\n~ ")
            password = input("Please enter your master password\n~ ")
            sql = "SELECT * FROM users WHERE username=%s AND password=%s;"
            val = (username, password)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                masterU = username
                f = 1
                break
            else:
                print("No such records found. Please try again!\n\n")
        if f == 1:
            break
while True:
    print("\n\n\n" + "-" * 90)
    print(("-" * 13) + "Welcome back " + masterU + ("-" * 13))
    print(
        "Do you want to store a new password or view your passwords? \n  1:Store New \n  2:View Saved \n  3:Update existing password \n  4:Exit the program"
    )
    n = int(input("~ "))
    print("-" * 90)
    if n == 1:
        print(
            "\n\nPlease give the following inputs to be stored locally. Dont worry. Your passwords are properly encrypted and safe with us.\n\n\n"
        )
        platform = input(
            "Please enter the platform or website for which you want to store the password\n~ "
        )
        username = input(
            "Please enter your username or email for the respective platform\n~ "
        )
        while True:
            password = input("Now please enter your password for this platform\n~ ")
            confirm = input("Please re-enter the password for confirmation\n~ ")
            if password == confirm:
                password = bytes(password, "utf-8")
                password = cipher_suite.encrypt(password)
                sql = "INSERT INTO " + masterU + " VALUES(%s,%s,%s,%s)"
                val = (platform, username, password, key)
                cursor.execute(sql, val)
                mydb.commit()
                print("\nPassword inserted Successfully\n\n")
                break
            else:
                print("\nPassword mismatch please re-enter\n\n")
    elif n == 2:
        while True:
            platform = input(
                "Please enter the platform or website for which you want to view the password\n~ "
            )
            username = input(
                "Please enter your username or email for the respective platform\n~ "
            )
            sql = (
                "SELECT password,crypt FROM "
                + masterU
                + " WHERE platform=%s AND username=%s"
            )
            val = (platform, username)
            cursor.execute(sql, val)
            password = cursor.fetchall()
            if len(password) > 0:
                for i in password:
                    x = bytes(i[0], "utf-8")
                    k = bytes(i[1], "utf-8")
                    cipher_suite1 = Fernet(k)
                    x = cipher_suite1.decrypt(x)
                    x = x.decode("utf-8")
                    print(f"\nThe required password for your account is {x}\n\n")
                break
            else:
                print("\nNo such entries found. Please enter again\n\n")
    elif n==3:
        while True:
            platform=input("Please enter the platform\n~ ")
            username = input(
                    "Please enter your username or email for the respective platform\n~ "
                )
            Oldpassword=input("Please enter your old password for this account\n~ ")
            sql = (
                    "SELECT password,crypt FROM "
                    + masterU
                    + " WHERE platform=%s AND username=%s"
                )
            val = (platform, username)
            cursor.execute(sql, val)
            password = cursor.fetchall()
            if len(password) > 0:
                crypt=bytes(password[0][1], "utf-8")
                cipher_suite1 = Fernet(crypt)
                while True:
                    Newpassword=input("Please enter the new password\n~ ")
                    confirm=input("Please re enter for confirmation\n~ ")
                    if Newpassword==confirm:
                        Newpassword=bytes(Newpassword,'utf-8')
                        passu=cipher_suite1.encrypt(Newpassword)
                        sql="UPDATE "+masterU+" SET password=%s WHERE username=%s AND platform=%s"
                        val=(passu,username,platform)
                        cursor.execute(sql,val)
                        mydb.commit()
                        print("Password changed successfully")
                        break
                    else:
                        print("Password mismatch found. Please try again")
                break
            else:
                print("No such records found. Please try again")

    elif n == 4:
        print("\nThank you for using the program. Hope it was useful for you :)")
        break
    else:
        print("\nYou have entered an invalid input. Please try again\n\n")
