"""
In-memory SQLite database initialization for access control threat demonstration.
"""
import sqlite3
import json
from typing import Optional


def init_database(db_path: str = ":memory:") -> sqlite3.Connection:
    """
    Initialize in-memory SQLite database with access control schema.
    
    Args:
        db_path: Database path (default: ":memory:" for in-memory DB)
    
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript("""
        -- Users table (Name, Role, Pass_Key)
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            pass_key TEXT NOT NULL UNIQUE
        );
        
        -- Doors table
        CREATE TABLE IF NOT EXISTS doors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            door_code TEXT NOT NULL UNIQUE,
            description TEXT
        );
        
        -- Door-PassKey mapping (which passkeys open which doors)
        CREATE TABLE IF NOT EXISTS door_passkeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            door_id INTEGER NOT NULL,
            pass_key TEXT NOT NULL,
            FOREIGN KEY (door_id) REFERENCES doors(id),
            UNIQUE(door_id, pass_key)
        );
    """)
    
    # Insert initial data
    # Users (5 distinct users)
    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, role, pass_key) VALUES (?, ?, ?)",
        [
            ('Bjorn', 'CEO', 'P578655'),
            ('Amit', 'Anarchist', 'P666666'),
            ('Sarah', 'Manager', 'P123456'),
            ('John', 'Developer', 'P789012'),
            ('Emma', 'Security', 'P345678')
        ]
    )
    
    # Doors
    cursor.executemany(
        "INSERT OR IGNORE INTO doors (door_code, description) VALUES (?, ?)",
        [
            ('A', 'Main Office'),
            ('B', 'Server Room'),
            ('C', 'Storage'),
            ('D', 'Lab'),
            ('E', 'Archive')
        ]
    )
    
    # Door-PassKey mappings
    # Door A opens with P578655 (Bjorn) OR P123456 (Sarah)
    cursor.executemany(
        "INSERT OR IGNORE INTO door_passkeys (door_id, pass_key) VALUES (?, ?)",
        [
            (1, 'P578655'),  # Door A accepts Bjorn's passkey
            (1, 'P123456')   # Door A also accepts Sarah's passkey
        ]
    )
    
    # Door B opens with P666666 (Amit) OR P789012 (John)
    cursor.executemany(
        "INSERT OR IGNORE INTO door_passkeys (door_id, pass_key) VALUES (?, ?)",
        [
            (2, 'P666666'),  # Door B accepts Amit's passkey
            (2, 'P789012')  # Door B also accepts John's passkey
        ]
    )
    
    # Door C opens with P345678 (Emma)
    cursor.execute(
        "INSERT OR IGNORE INTO door_passkeys (door_id, pass_key) VALUES (?, ?)",
        (3, 'P345678')
    )
    
    # Door D opens with P123456 (Sarah) OR P789012 (John)
    cursor.executemany(
        "INSERT OR IGNORE INTO door_passkeys (door_id, pass_key) VALUES (?, ?)",
        [
            (4, 'P123456'),  # Door D accepts Sarah's passkey
            (4, 'P789012')  # Door D also accepts John's passkey
        ]
    )
    
    # Door E opens with P345678 (Emma)
    cursor.execute(
        "INSERT OR IGNORE INTO door_passkeys (door_id, pass_key) VALUES (?, ?)",
        (5, 'P345678')
    )
    
    conn.commit()
    return conn


def get_db_connection(db_path: str = ":memory:") -> sqlite3.Connection:
    """
    Get or create database connection.
    For in-memory DB, creates new connection each time.
    For file-based DB, reuses existing connection.
    
    Args:
        db_path: Database path (":memory:" for in-memory)
    
    Returns:
        SQLite connection
    """
    if db_path == ":memory:":
        # Always create new in-memory DB
        return init_database(":memory:")
    else:
        # File-based DB - check if exists, create if not
        import os
        if not os.path.exists(db_path):
            return init_database(db_path)
        else:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn


# Global in-memory database connection (initialized on module import)
_db_conn: Optional[sqlite3.Connection] = None


def get_shared_db() -> sqlite3.Connection:
    """
    Get shared in-memory database connection.
    Creates connection on first call, reuses afterwards.
    
    Returns:
        SQLite connection
    """
    global _db_conn
    if _db_conn is None:
        _db_conn = init_database(":memory:")
    return _db_conn


if __name__ == "__main__":
    # Test database initialization
    conn = init_database(":memory:")
    cursor = conn.cursor()
    
    # Test queries
    print("=== Users ===")
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(dict(row))
    
    print("\n=== Doors ===")
    cursor.execute("SELECT * FROM doors")
    for row in cursor.fetchall():
        print(dict(row))
    
    print("\n=== Door Access (Who can open Door A?) ===")
    cursor.execute("""
        SELECT DISTINCT u.name, u.role, u.pass_key
        FROM users u
        JOIN door_passkeys dp ON u.pass_key = dp.pass_key
        JOIN doors d ON dp.door_id = d.id
        WHERE d.door_code = 'A'
    """)
    for row in cursor.fetchall():
        print(dict(row))
    
    conn.close()

