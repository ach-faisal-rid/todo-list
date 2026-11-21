# config.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # user default XAMPP/Laragon
        password="root",          # biasanya kosong di XAMPP
        database="db_todo"
    )