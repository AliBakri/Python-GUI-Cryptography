import sqlite3 as sq
import os
import hashlib
import uuid

DATABASE_NAME = 'LOGS.db'

# Creating the Database, This function is called at each run
def createDatabse():
    # Validating if database file exists
    if os.path.isfile(DATABASE_NAME):
        pass
    else:
        # If the database file does not exist create it and its tables
        # Creating connection
        conn = sq.connect(DATABASE_NAME)
        # Creating Cursor object
        c = conn.cursor()
        # Executing the table creation Queries
        c.execute("""
                     CREATE TABLE CAESER_CIPHER(
                     ID INTEGER PRIMARY KEY,
                     OPTION_TYPE TEXT,
                     CIPHER TEXT,
                     KEY INTEGER,
                     MESSAGE TEXT,
                     TIMESTAMP TEXT
                  )""")
        c.execute("""
                     CREATE TABLE RAILFENCE(
                     ID INTEGER PRIMARY KEY,
                     OPTION_TYPE TEXT,
                     PASSWORD TEXT,
                     CIPHER TEXT,
                     MESSAGE TEXT,
                     TIMESTAMP TEXT
                  )""")
        c.execute("""
                     CREATE TABLE CREDENTIALS(
                     ID INTEGER PRIMARY KEY,    
                     USERNAME TEXT,
                     SALT BLOB,
                     PASSWORD BLOB,
                     EMAIL TEXT,
                     RGB_PATTERN TEXT,
                     PICTURE_ORDER TEXT             
                   )""")
        # Commiting changes and closing connection
        conn.commit()
        conn.close()

# Adding Caeser Cipher Log
def add_Caeser_cipher(alType, cipher, key, message, timestamp):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO CAESER_CIPHER (OPTION_TYPE, CIPHER, KEY, MESSAGE, TIMESTAMP) VALUES (?,?,?,?,?)",
                 (alType, cipher, key, message, timestamp,))
    conn.commit()
    conn.close()

# Adding Railfence Log
def add_RailFence(type, password, cipher, message, timestamp):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO RAILFENCE (OPTION_TYPE, PASSWORD, CIPHER, MESSAGE, TIMESTAMP) VALUES (?,?,?,?,?)",
              (type, password, cipher, message, timestamp))
    conn.commit()
    conn.close()

# Getting caeser Cipher logs
def get_CaeserCipherLog():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CAESER_CIPHER")
    logs = c.fetchall()
    conn.close()
    return logs

# Getting Railfence Logs
def get_RailFenceLog():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM RAILFENCE")
    logs = c.fetchall()
    conn.close()
    return logs

# Clearing Logs
def clear_all_logs():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM CAESER_CIPHER")
    c.execute("DELETE FROM RAILFENCE")
    conn.commit()
    conn.close()

# Getting Caeser Cipher log per ID
def get_CaeserCipherLogPerID(id):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CAESER_CIPHER WHERE ID = (?)", (id),)
    log = c.fetchone()
    return log

# Getting Caeser Cipher log peR ID
def get_RailFenceLogPerID(id):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM RAILFENCE WHERE ID = (?)", (id,))
    log = c.fetchone()
    return log

# Creating A user
def createUser(username, password, email, RGB, PictureOrder):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    # Encoding Password for hashing
    encodedPass = str(password).encode()
    # Each user has a specific Salt added for the password for hashing
    # Account Password is salted then hashed for maximum security
    salt = uuid.uuid4().bytes
    # Creating the hashed password
    hashedpass = hashlib.sha512(encodedPass+salt).digest()
    c.execute("INSERT INTO CREDENTIALS (USERNAME, SALT, PASSWORD, EMAIL, RGB_PATTERN, PICTURE_ORDER) VALUES (?,?,?,?,?,?)"
              ,(username,salt, hashedpass, email, RGB, PictureOrder,))
    conn.commit()
    conn.close()

# Checking if there's a user registered
def defaultUserExists():
    conn=sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CREDENTIALS")
    values = c.fetchall()
    # The Credentials table will only have one entry with ID of 1
    # We try to fetch the row at ID 1
    # if the returned value is not 0, a User exists
    return len(values) != 0

# validating login
def validate(username, password):
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    # Fetching Row by username
    c.execute("SELECT * FROM CREDENTIALS WHERE USERNAME = (?)", (username,))
    # Checking if username exists
    v = c.fetchall()
    if len(v) == 0:
        return False
    else:
        # We take the user salt, add it to the input password then hash it with same hashing method
        # if the inputed salted hashed password and the saved hashed password match then the login is successful
        salt = v[0][2]
        encodedPassword = str(password).encode()
        hashedPassword = hashlib.sha512(encodedPassword+salt).digest()
        return v[0][3] == hashedPassword

# removing the user
def removeUser():
    conn=sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM CREDENTIALS")
    conn.commit()
    conn.close()

# getting user
def getUser():
    conn = sq.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM CREDENTIALS WHERE ID = 1")
    v = c.fetchall()
    return v