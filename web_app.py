import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="WIUT Digital Health Portal", page_icon="📱")

def load_questions():
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except:
        return None

# --- APP UI ---
st.title("📱 Social Media Dependency Assessment")
st.write("Welcome! This friendly tool helps you understand your digital habits. 🎈")

# Sidebar for Registration
st.sidebar.header("User Registration")
name = st.sidebar.text_input("Full Name", placeholder="e.g. Gulnora")
student_id = st.sidebar.text_input("Student ID", placeholder="00024619")

# Load Questions
data = load_questions()

if data and name and student_id:
    st.info(f"Hi {name}! Please answer these 20 questions about your digital life. ✨")
    
    total_score = 0
    with st.form("survey_form"):
        # Display questions
        for q in data['questions']:
            options = list(q['options'].keys())
            selection = st.radio(f"**Q{q['id']}: {q['text']}**", options)
            total_score += q['options'][selection]
        
        submitted = st.form_submit_button("Generate My Friendly Report 🚀")

    if submitted:
        # Scoring and Detailed Logic
        percentage = (total_score / 80) * 100
        
        # Determine Status, Advice, and Color
        if total_score <= 15:
            status, color, icon = "Digital Minimalist", "green", "🌿"
            advice = "Incredible! You have a super healthy relationship with your phone. Keep enjoying the real world!"
        elif total_score <= 30:
            status, color, icon = "Casual User", "blue", "✅"
            advice = f"Great job, {name}! You use social media as a tool, but it doesn't run your life. Keep up those healthy boundaries."
        elif total_score <= 45:
            status, color, icon = "Balanced Dependency", "orange", "⚖️"
            advice = "You're doing okay, but you might be scrolling mindlessly sometimes. Why not try a 'no-phone' hour tonight?"
        elif total_score <= 60:
            status, color, icon = "High Dependency", "orange", "⚠️"
            advice = "You're spending quite a bit of time online. Try deleting one social app for a few days to see how you feel!"
        elif total_score <= 75:
            status, color, icon = "At-Risk", "red", "🚨"
            advice = "It looks like your phone is taking up a lot of your energy. We recommend a 24-hour digital detox this weekend."
        else:
            status, color, icon = "Critical State", "red", "🆘"
            advice = "Warning: Your digital habits are impacting your happiness. Please reach out to a friend or mentor to talk about a lifestyle change."

        # Visual Effects
        st.balloons()
        
        # Display Friendly Report
        st.markdown(f"### {icon} Your Results are In!")
        
        # Color-coded result box
        if color == "green": st.success(f"**Status: {status}**")
        elif color == "blue": st.info(f"**Status: {status}**")
        elif color == "orange": st.warning(f"**Status: {status}**")
        else: st.error(f"**Status: {status}**")

        st.write(f"**Dependency Level:** {percentage:.2f}%")
        st.write(f"**A Note for you:** {advice}")
        
        st.divider()
        st.write("📁 **Want to keep this?** Download your report file below:")
        result_json = json.dumps({
            "Name": name, 
            "ID": student_id, 
            "Score": total_score, 
            "Status": status,
            "Advice": advice
        }, indent=4)
        st.download_button("Download results.json", result_json, file_name="my_digital_report.json")

else:
    st.warning("Please enter your Name and Student ID in the sidebar on the left to start your journey! 👈")
