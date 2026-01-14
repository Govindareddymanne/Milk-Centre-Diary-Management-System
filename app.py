import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import calendar

# ================= CONSTANT RATE =================
RATE = 7  # Fixed rate used by milk centre

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Govind@123",
        database="milk_center"
    )

# ---------------- PDF GENERATION ----------------
def generate_bill_pdf(name, start_date, end_date, total_milk, total_amount):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Milk Centre - Farmer Bill")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Farmer Name : {name}")
    c.drawString(50, 740, f"Billing Period : {start_date} to {end_date}")
    c.drawString(50, 720, f"Total Milk Supplied : {total_milk:.2f} Liters")
    c.drawString(50, 700, f"Total Amount Payable : ₹ {total_amount:.2f}")

    c.drawString(50, 660, "Thank you for your milk supply.")
    c.drawString(50, 640, "— Milk Centre")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="Milk Centre Diary", layout="wide")
st.title("🥛 Milk Centre Diary Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Farmer Registration",
        "Milk Entry",
        "Reports",
        "Billing (15 Days)"
    ]
)

# ================= FARMER REGISTRATION =================
if menu == "Farmer Registration":
    st.header("👨‍🌾 Farmer Registration")

    name = st.text_input("Farmer Name")
    mobile = st.text_input("Mobile Number")
    village = st.text_input("Village")

    if st.button("Register Farmer"):
        if not name or not mobile or not village:
            st.error("Please fill all fields")
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO farmers (name, mobile, village) VALUES (%s,%s,%s)",
                (name, mobile, village)
            )
            db.commit()
            st.success("✅ Farmer registered successfully")

# ================= MILK ENTRY =================
elif menu == "Milk Entry":
    st.header("📒 Daily Milk Entry")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM farmers")
    farmers = cur.fetchall()

    if not farmers:
        st.warning("Please register farmers first")
    else:
        farmer_map = {f"{f['farmer_id']} - {f['name']}": f for f in farmers}
        farmer_key = st.selectbox("Select Farmer", farmer_map.keys())
        farmer = farmer_map[farmer_key]

        entry_date = st.date_input("Date", date.today())
        session = st.selectbox("Session", ["Morning", "Evening"])
        quantity = st.number_input("Quantity (Liters)", min_value=0.0)
        fat = st.number_input("Fat Percentage", min_value=0.0)

        if st.button("Submit Milk Entry"):
            # 🔒 Prevent duplicate Morning/Evening entry
            cur.execute("""
                SELECT COUNT(*) AS cnt
                FROM milk_collection
                WHERE farmer_id=%s AND date=%s AND session=%s
            """, (farmer["farmer_id"], str(entry_date), session))
            exists = cur.fetchone()["cnt"]

            if exists > 0:
                st.error(
                    f"❌ {session} entry already exists for {entry_date}. "
                    "Only one Morning and one Evening entry allowed."
                )
            else:
                amount = quantity * fat * RATE

                cur.execute("""
                    INSERT INTO milk_collection
                    (farmer_id, date, session, quantity, fat, rate, amount)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    farmer["farmer_id"],
                    str(entry_date),
                    session,
                    quantity,
                    fat,
                    RATE,
                    amount
                ))
                db.commit()

                st.success(
                    f"✅ {session} entry saved | Amount ₹ {amount:.2f}"
                )

# ================= REPORTS =================
elif menu == "Reports":
    st.header("📊 Reports")

    report_type = st.radio(
        "Select Report Type",
        ["Daily Report", "Date-Range Report"]
    )

    db = get_db()
    cur = db.cursor(dictionary=True)

    # -------- DAILY REPORT --------
    if report_type == "Daily Report":
        selected_date = st.date_input("Select Date", date.today())

        cur.execute("""
            SELECT f.name, m.session, m.quantity, m.fat, m.amount
            FROM milk_collection m
            JOIN farmers f ON f.farmer_id = m.farmer_id
            WHERE m.date = %s
            ORDER BY f.name, m.session
        """, (str(selected_date),))

        data = cur.fetchall()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.subheader("📈 Farmer-wise Earnings")
            st.bar_chart(df.groupby("name")["amount"].sum())
        else:
            st.warning("No records found for this date")

    # -------- DATE-RANGE REPORT --------
    else:
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        if start_date > end_date:
            st.error("Start date must be before end date")
        else:
            cur.execute("""
                SELECT f.name, m.date, m.session, m.quantity, m.fat, m.amount
                FROM milk_collection m
                JOIN farmers f ON f.farmer_id = m.farmer_id
                WHERE m.date BETWEEN %s AND %s
                ORDER BY m.date, f.name
            """, (str(start_date), str(end_date)))

            data = cur.fetchall()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
                st.metric("Total Amount", f"₹ {df['amount'].sum():.2f}")
            else:
                st.warning("No data found for selected period")

# ================= BILLING (AUTO 15 DAYS) =================
else:
    st.header("🧾 Individual Farmer Billing (15 Days)")

    today = date.today()
    year, month = today.year, today.month
    last_day = calendar.monthrange(year, month)[1]

    cycle = st.radio("Billing Cycle", ["1–15", "16–Month End"])

    if cycle == "1–15":
        start_date = date(year, month, 1)
        end_date = date(year, month, 15)
    else:
        start_date = date(year, month, 16)
        end_date = date(year, month, last_day)

    st.info(f"Billing Period: {start_date} to {end_date}")

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM farmers")
    farmers = cur.fetchall()

    farmer = st.selectbox(
        "Select Farmer",
        farmers,
        format_func=lambda f: f["name"]
    )

    cur.execute("""
        SELECT SUM(quantity) AS total_milk,
               SUM(amount) AS total_amount
        FROM milk_collection
        WHERE farmer_id=%s AND date BETWEEN %s AND %s
    """, (farmer["farmer_id"], str(start_date), str(end_date)))

    result = cur.fetchone()

    if result and result["total_amount"]:
        st.metric("Total Milk (Liters)", f"{result['total_milk']:.2f}")
        st.metric("Total Amount", f"₹ {result['total_amount']:.2f}")

        pdf = generate_bill_pdf(
            farmer["name"],
            start_date,
            end_date,
            result["total_milk"],
            result["total_amount"]
        )

        st.download_button(
            "⬇️ Download PDF Bill",
            pdf,
            file_name=f"bill_{farmer['name']}_{start_date}_{end_date}.pdf",
            mime="application/pdf"
        )

        if st.button("📩 Send SMS (Simulated)"):
            st.success(
                f"SMS sent to {farmer['mobile']}:\n"
                f"Your milk bill amount is ₹ {result['total_amount']:.2f}"
            )
    else:
        st.warning("No records for this farmer in selected billing period")