import sqlite3
import time
from app import DB_PATH

conn = sqlite3.connect(DB_PATH)
rows = conn.execute(
    "SELECT username, password_hash, failed_attempts, locked_until FROM users"
).fetchall()
conn.close()

if not rows:
    print("No users yet.")
for username, pw_hash, attempts, locked_until in rows:
    remianing = max(0, int(locked_until - time.time()))
    print(f"username        : {username}")
    print(f"password_hash   : {pw_hash}")
    print(f"failed_attempts : {attempts}")
    print(f"locked          : {'YES (' + str(remianing) + 's left)' if remianing else 'no'}")
    print("-" * 70)