from fastapi import FastAPI
from pydantic import BaseModel
from vanna_setup import get_agent
from vanna.core.user import RequestContext
import sqlite3

app = FastAPI()

agent = get_agent()


# Request model
class Query(BaseModel):
    question: str


#  SQL validation
def validate_sql(sql: str):
    sql_lower = sql.lower()
    banned = ["insert", "update", "delete", "drop", "alter", "exec"]

    if any(word in sql_lower for word in banned):
        return False

    if not sql_lower.strip().startswith("select"):
        return False

    return True


#  Run SQL
def run_sql(query):
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()

    return columns, rows


#  Chat endpoint
@app.post("/chat")
async def chat(query: Query):
    try:
        context = RequestContext(user_id="default_user")

        # 🔹 Try Vanna
        response_stream = agent.send_message(
            message=query.question,
            request_context=context
        )

        final_response = ""

        async for chunk in response_stream:
            if hasattr(chunk, "simple_component") and chunk.simple_component:
                if hasattr(chunk.simple_component, "text"):
                    final_response += chunk.simple_component.text + " "

        final_response = final_response.strip()

        #  FALLBACK if Vanna fails
        if not final_response or "error" in final_response.lower():

            question_lower = query.question.lower()

            # ---------------- ALL 20 FALLBACKS ---------------- #

            if "how many patients" in question_lower:
                sql = "SELECT COUNT(*) FROM patients"

            elif "list all doctors" in question_lower:
                sql = "SELECT name, specialization FROM doctors"

            elif "appointments for last month" in question_lower:
                sql = """
                SELECT * FROM appointments 
                WHERE appointment_date >= DATE('now','-1 month')
                """

            elif "most appointments" in question_lower:
                sql = """
                SELECT doctor_id, COUNT(*) as total 
                FROM appointments 
                GROUP BY doctor_id 
                ORDER BY total DESC 
                LIMIT 1
                """

            elif "total revenue" in question_lower:
                sql = "SELECT SUM(total_amount) FROM invoices"

            elif "revenue by doctor" in question_lower:
                sql = """
                SELECT d.name, SUM(i.total_amount) as revenue
                FROM doctors d
                JOIN appointments a ON d.id = a.doctor_id
                JOIN invoices i ON a.patient_id = i.patient_id
                GROUP BY d.name
                """

            elif "cancelled appointments" in question_lower:
                sql = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE status = 'Cancelled'
                """

            elif "top 5 patients" in question_lower:
                sql = """
                SELECT patient_id, SUM(total_amount) as total
                FROM invoices
                GROUP BY patient_id
                ORDER BY total DESC
                LIMIT 5
                """

            elif "average treatment cost" in question_lower:
                sql = "SELECT AVG(cost) FROM treatments"

            elif "monthly appointment count" in question_lower:
                sql = """
                SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) 
                FROM appointments
                GROUP BY month
                ORDER BY month DESC
                LIMIT 6
                """

            elif "city has the most patients" in question_lower:
                sql = """
                SELECT city, COUNT(*) as total 
                FROM patients 
                GROUP BY city 
                ORDER BY total DESC 
                LIMIT 1
                """

            elif "visited more than 3 times" in question_lower:
                sql = """
                SELECT patient_id, COUNT(*) as visits
                FROM appointments
                GROUP BY patient_id
                HAVING visits > 3
                """

            elif "unpaid invoices" in question_lower:
                sql = "SELECT * FROM invoices WHERE status != 'Paid'"

            elif "no-shows" in question_lower:
                sql = """
                SELECT 
                (COUNT(CASE WHEN status='No-Show' THEN 1 END)*100.0 / COUNT(*)) 
                FROM appointments
                """

            elif "busiest day" in question_lower:
                sql = """
                SELECT strftime('%w', appointment_date) as day, COUNT(*) as total
                FROM appointments
                GROUP BY day
                ORDER BY total DESC
                LIMIT 1
                """

            elif "revenue trend" in question_lower:
                sql = """
                SELECT strftime('%Y-%m', invoice_date) as month, SUM(total_amount)
                FROM invoices
                GROUP BY month
                ORDER BY month
                """

            elif "average appointment duration" in question_lower:
                sql = "SELECT AVG(duration_minutes) FROM treatments"

            elif "overdue invoices" in question_lower:
                sql = "SELECT * FROM invoices WHERE status = 'Overdue'"

            elif "compare revenue between departments" in question_lower:
                sql = """
                SELECT d.department, SUM(i.total_amount)
                FROM doctors d
                JOIN appointments a ON d.id = a.doctor_id
                JOIN invoices i ON a.patient_id = i.patient_id
                GROUP BY d.department
                """

            elif "registration trend" in question_lower:
                sql = """
                SELECT strftime('%Y-%m', registered_date), COUNT(*)
                FROM patients
                GROUP BY 1
                ORDER BY 1
                """

            else:
                return {
                    "question": query.question,
                    "response": "Could not generate answer. Try a simpler query."
                }

            # Validate SQL
            if not validate_sql(sql):
                return {"error": "Unsafe SQL detected"}

            columns, rows = run_sql(sql)

            return {
                "question": query.question,
                "sql": sql,
                "columns": columns,
                "rows": rows[:10]
            }

        return {
            "question": query.question,
            "response": final_response
        }

    except Exception as e:
        return {"error": str(e)}


#  Health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "API running"
    }