import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

DB_NAME = "clinic.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT
    )
    """)

    conn.commit()


def random_date_within_last_year():
    days_ago = random.randint(0, 365)
    return datetime.now() - timedelta(days=days_ago)


def insert_doctors(conn):
    cursor = conn.cursor()

    specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

    for _ in range(15):
        cursor.execute("""
        INSERT INTO doctors (name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
        """, (
            fake.name(),
            random.choice(specializations),
            random.choice(specializations),
            fake.phone_number()
        ))

    conn.commit()


def insert_patients(conn):
    cursor = conn.cursor()
    cities = ["Mumbai", "Pune", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Kolkata", "Ahmedabad"]

    for _ in range(200):
        cursor.execute("""
        INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fake.first_name(),
            fake.last_name(),
            fake.email() if random.random() > 0.2 else None,
            fake.phone_number() if random.random() > 0.2 else None,
            fake.date_of_birth(minimum_age=18, maximum_age=80),
            random.choice(["M", "F"]),
            random.choice(cities),
            random_date_within_last_year().date()
        ))

    conn.commit()


def insert_appointments(conn):
    cursor = conn.cursor()

    statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]

    for _ in range(500):
        cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 200),
            random.randint(1, 15),
            random_date_within_last_year(),
            random.choice(statuses),
            fake.text() if random.random() > 0.3 else None
        ))

    conn.commit()


def insert_treatments(conn):
    cursor = conn.cursor()

    for _ in range(350):
        cursor.execute("""
        INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
        VALUES (?, ?, ?, ?)
        """, (
            random.randint(1, 500),
            fake.word(),
            round(random.uniform(50, 5000), 2),
            random.randint(10, 120)
        ))

    conn.commit()


def insert_invoices(conn):
    cursor = conn.cursor()

    statuses = ["Paid", "Pending", "Overdue"]

    for _ in range(300):
        total = round(random.uniform(100, 5000), 2)
        paid = total if random.random() > 0.3 else round(random.uniform(0, total), 2)

        cursor.execute("""
        INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
        VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 200),
            random_date_within_last_year().date(),
            total,
            paid,
            random.choice(statuses)
        ))

    conn.commit()


def main():
    conn = create_connection()

    create_tables(conn)
    insert_doctors(conn)
    insert_patients(conn)
    insert_appointments(conn)
    insert_treatments(conn)
    insert_invoices(conn)

    print(" Database created successfully!")
    print(" 15 doctors")
    print(" 200 patients")
    print(" 500 appointments")
    print(" 350 treatments")
    print(" 300 invoices")

    conn.close()


if __name__ == "__main__":
    main()