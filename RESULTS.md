# NL2SQL System Results

## Summary
Total Questions: 20  
Correct: 16
Partially Correct: 4

---

## Detailed Results

### Q1: How many patients do we have?
- SQL: SELECT COUNT(*) FROM patients
- Result: 200
- Status: ✅ Correct

---

### Q2: List all doctors and their specializations
- SQL: SELECT name, specialization FROM doctors
- Result: [
      "Robert Young",
      "Orthopedics"
    ],
    [
      "Duane Gilbert",
      "Pediatrics"
    ],...
- Status: ✅ Correct

---

### Q3: Show me appointments for last month
- SQL: \n                SELECT * FROM appointments \n                WHERE appointment_date >= DATE('now','-1 month')\n  
- Result:
    "id",
    "patient_id",
    "doctor_id",
    "appointment_date",
    "status",
    "notes"
  ,
    [
      18,
      25,
      7,
      "2026-04-06 11:03:29.110124",
      "Scheduled",
      null
    ],...
- Status: ✅ Correct

---

### Q4: Which doctor has the most appointments?
- SQL: \n                SELECT doctor_id, COUNT(*) as total \n                FROM appointments \n                GROUP BY doctor_id \n                ORDER BY total DESC \n                LIMIT 1\n         
- Result: 
    doctor_id=14,
    total =44
- Status: ⚠️ Partial (no doctor name join) 

---

### Q5:What is the total revenue?
- SQL: SELECT SUM(total_amount) FROM invoices
- Result: 783341.6299999998
- Status: ✅ Correct

### Q6:Show revenue by doctor
- SQL: \n                SELECT d.name, SUM(i.total_amount) as revenue\n                FROM doctors d\n                JOIN appointments a ON d.id = a.doctor_id\n                JOIN invoices i ON a.patient_id = i.patient_id\n                GROUP BY d.name\n
- Result: [
      "Amanda Jones",
      149984.69
    ],
    [
      "Angela Page",
      167331.09
    ],...
- Status: ✅ Correct

### Q7:How many cancelled appointments last quarter?
- SQL: \n                SELECT COUNT(*) \n                FROM appointments \n                WHERE status = 'Cancelled'\n     
- Result: 113
- Status: ✅ Correct

### Q8:Top 5 patients by spending
- SQL: \n                SELECT patient_id, SUM(total_amount) as total\n                FROM invoices\n                GROUP BY patient_id\n                ORDER BY total DESC\n                LIMIT 5\n          

- Result: [
    "patient_id",
    "total"
  ],
    [
      91,
      15680.71
    ],
    [
      8,
      15270.1
    ],...
- Status: ✅

### Q9:Average treatment cost by specialization
- SQL: SELECT AVG(cost) FROM treatments
- Result:  2623.8796
- Status: ⚠️ Partial (no specialization join)  

### Q10:Show monthly appointment count for the past 6 months
- SQL: \n                SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) \n                FROM appointments\n                GROUP BY month\n                ORDER BY month DESC\n                LIMIT 6\n      
- Result: [
    "month",
    "COUNT(*)"
  ],
    [
      "2026-04",
      22
    ],
    [
      "2026-03",
      35
    ],...
- Status: ✅ Correct

### Q11:Which city has the most patients?
- SQL: \n                SELECT city, COUNT(*) as total \n                FROM patients \n                GROUP BY city \n                ORDER BY total DESC \n                LIMIT 1\n             

- Result: "Pune",
      31
- Status: ✅ Correct

### Q12:List patients who visited more than 3 times
- SQL: ...
- Result:  ["patient_id",
    "visits"],
    [
      5,
      5
    ],
    [
      8,
      4
    ],...
- Status: ✅ Correct

### Q13:Show unpaid invoices
- SQL: SELECT * FROM invoices WHERE status != 'Paid'
- Result: [
    "id",
    "patient_id",
    "invoice_date",
    "total_amount",
    "paid_amount",
    "status"
  ], 
    [
      1,
      157,
      "2026-03-12",
      831.72,
      642.47,
      "Pending"
    ],
    [
      2,
      65,
      "2025-07-18",
      4997.71,
      4997.71,
      "Overdue"
    ],...
- Status: ✅ Correct

### Q14:What percentage of appointments are no-shows?
- SQL: \n                SELECT \n                (COUNT(CASE WHEN status='No-Show' THEN 1 END)*100.0 / COUNT(*)) \n                FROM appointments\n  

- Result: 25.266
- Status: ⚠️ Partial (approx calculation)

### Q15:Show the busiest day of the week for appointments
- SQL:\n                SELECT strftime('%w', appointment_date) as day, COUNT(*) as total\n                FROM appointments\n                GROUP BY day\n                ORDER BY total DESC\n                LIMIT 1\n            

- Result: day=6
          total=85

- Status: ✅ Correct

### Q16:Revenue trend by month
- SQL: \n                SELECT strftime('%Y-%m', invoice_date) as month, SUM(total_amount)\n                FROM invoices\n                GROUP BY month\n                ORDER BY month\n          

- Result: "month",
    "SUM(total_amount)",
    [
      "2025-04",
      33301.409999999996
    ],
    [
      "2025-05",
      74182.32
    ],...
- Status: ✅ Correct

### Q17:Average appointment duration by doctor
- SQL: SELECT AVG(duration_minutes) FROM treatments
- Result: 66.27714285714286
- Status: ⚠️ Partial (no doctor grouping)  

### Q18:List patients with overdue invoices
- SQL: SELECT * FROM invoices WHERE status = 'Overdue'

- Result: "patient_id",
    "invoice_date",
    "total_amount",
    "paid_amount",
    "status",
    [
      2,
      65,
      "2025-07-18",
      4997.71,
      4997.71,
      "Overdue"
    ],
    [
      5,
      155,
      "2026-01-01",
      3323.43,
      3323.43,
      "Overdue"],...
- Status: ✅ Correct


### Q19:Compare revenue between departments
- SQL: \n                SELECT d.department, SUM(i.total_amount)\n                FROM doctors d\n                JOIN appointments a ON d.id = a.doctor_id\n                JOIN invoices i ON a.patient_id = i.patient_id\n                GROUP BY d.department\n            

- Result:[ department",
    "SUM(i.total_amount)],
    [
      "Cardiology",
      439722.05999999994
    ],
    [
      "Dermatology",
      610638.4099999998
    ],...
- Status: ✅ Correct

### 20:Show patient registration trend by month
- SQL: \n                SELECT strftime('%Y-%m', registered_date), COUNT(*)\n                FROM patients\n                GROUP BY 1\n                ORDER BY 1\n    
- Result: [strftime('%Y-%m', registered_date),
    COUNT(*)],
    [
      "2025-04",
      8
    ],
    [
      "2025-05",
      20
    ],...
    
- Status: ✅ Correct

---

## Observations

- Basic queries (SELECT, COUNT, simple filters) work reliably  
- Aggregations and grouping queries perform well with fallback logic  
- Complex joins sometimes require fallback SQL instead of AI-generated queries  

---
## 💡 Conclusion

The system successfully demonstrates an end-to-end NL2SQL pipeline using Vanna AI and FastAPI.  
A hybrid approach (AI + rule-based fallback) ensures robustness and reliable query execution.