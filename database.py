# database.py
import sqlite3
import os

DB_NAME = "vehicles.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Crea las tablas owners y vehicles si no existen.
    Se puede llamar al inicio de la app sin problemas.
    """
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL UNIQUE,
            brand TEXT,
            model TEXT,
            year INTEGER,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES owners (id)
        );
    """)

    conn.commit()
    conn.close()
