import asyncio
from vanna_setup import get_agent

agent = get_agent()


async def seed_memory():
    memory = agent.agent_memory

    #  Schema first
    await memory.save_text_memory(
        """
Database Schema:

Table: patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)

Table: doctors(id, name, specialization, department, phone)

Table: appointments(id, patient_id, doctor_id, appointment_date, status, notes)

Table: treatments(id, appointment_id, treatment_name, cost, duration_minutes)

Table: invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)
""",
        "schema"
    )

    examples = [
        ("How many patients do we have?", "SELECT COUNT(*) FROM patients"),
        ("List all patients", "SELECT * FROM patients"),
        ("Show female patients", "SELECT * FROM patients WHERE gender = 'F'"),
        ("List all doctors", "SELECT * FROM doctors"),
        ("Show completed appointments", "SELECT * FROM appointments WHERE status = 'Completed'")
    ]

    for q, sql in examples:
        await memory.save_text_memory(
            f"Question: {q}\nSQL: {sql}",
            "training_data"
        )

    print(" Seeded memory successfully!")


if __name__ == "__main__":
    asyncio.run(seed_memory())