import bcrypt

from utils.database import conn, cursor

# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):

    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

# ==========================================
# SIGNUP FUNCTION
# ==========================================

def signup(username, password):

    hashed_password = hash_password(password)

    try:

        cursor.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()

        return True

    except:

        return False

# ==========================================
# LOGIN FUNCTION
# ==========================================

def login(username, password):

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    data = cursor.fetchone()

    if data:

        stored_password = data[0]

        if bcrypt.checkpw(
            password.encode('utf-8'),
            stored_password
        ):

            return True

    return False