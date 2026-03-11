import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="WIUT Digital Health Portal", page_icon="🌐")

def load_questions():
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except:
        return None

# --- APP UI ---
st.title("🌐 Social Media Dependency Assessment")
st.write("This tool evaluates your digital well-being based on the SMD Scale.")

# Sidebar for Registration
st.sidebar.header("User Registration")
name = st.sidebar.text_input("Full Name")
student_id = st.sidebar.text_input("Student ID")

# Load Questions
data = load_questions()

if data and name and student_id:
    st.info(f"Welcome, {name}. Please answer the questions below.")
    
    total_score = 0
    with st.form("survey_form"):
        for q in data['questions']:
            options = list(q['options'].keys())
            selection = st.radio(f"Q{q['id']}: {q['text']}", options)
            total_score += q['options'][selection]
        
        submitted = st.form_submit_state = st.form_submit_button("Generate Report")

    if submitted:
        # Scoring Logic
        percentage = (total_score / 80) * 100
        if total_score <= 15: status = "Digital Minimalist"
        elif total_score <= 30: status = "Casual User"
        elif total_score <= 45: status = "Balanced Dependency"
        elif total_score <= 60: status = "High Dependency"
        elif total_score <= 75: status = "At-Risk"
        else: status = "Critical"

        st.success(f"### Result: {status}")
        st.metric("Dependency Level", f"{percentage:.2f}%")
        
        # Save Button (Simulated for Web)
        st.write("Your report is ready. You can download your results below.")
        result_json = json.dumps({"Name": name, "ID": student_id, "Score": total_score, "Status": status}, indent=4)
        st.download_button("Download results.json", result_json, file_name="web_results.json")

else:
    st.warning("Please enter your Name and Student ID in the sidebar to start.")