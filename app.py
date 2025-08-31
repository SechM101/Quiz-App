import streamlit as st
import os
from datetime import datetime, timedelta
import time
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Quiz App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    """Initialize Supabase client with environment variables"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Missing Supabase credentials. Please check your .env file.")
        st.stop()
    
    return create_client(url, key)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Database functions
def create_tables(supabase: Client):
    """Create necessary tables if they don't exist"""
    try:
        # This would typically be done through Supabase migrations
        # For now, we'll handle table creation through the UI
        pass
    except Exception as e:
        st.error(f"Error creating tables: {e}")

def seed_sample_questions(supabase: Client):
    """Seed the database with sample accounting questions"""
    sample_questions = [
        {
            "question": "According to IFRS 15, when should revenue be recognized?",
            "option_a": "When cash is received",
            "option_b": "When performance obligations are satisfied",
            "option_c": "When the contract is signed",
            "option_d": "When the invoice is sent",
            "correct_answer": "b",
            "explanation": "IFRS 15 requires revenue to be recognized when performance obligations are satisfied, not necessarily when cash is received.",
            "category": "IFRS 15"
        },
        {
            "question": "In Xero, when an obligation is not satisfied but payment is received, what should be recorded?",
            "option_a": "Revenue and Cash",
            "option_b": "Prepayment in bank account & Deferred Revenue",
            "option_c": "Accounts Receivable",
            "option_d": "Expense and Cash",
            "correct_answer": "b",
            "explanation": "When payment is received before the obligation is satisfied, it should be recorded as a prepayment (asset) and deferred revenue (liability).",
            "category": "Xero and Accounting Standards"
        },
        {
            "question": "What is the Matching Concept in accounting?",
            "option_a": "Matching expenses with revenue in the same period",
            "option_b": "Matching assets with liabilities",
            "option_c": "Matching debits with credits",
            "option_d": "Matching cash inflows with outflows",
            "correct_answer": "a",
            "explanation": "The Matching Concept requires that expenses be recognized in the same period as the revenue they help generate.",
            "category": "Matching Concept"
        },
        {
            "question": "How should foreign currency transactions be initially recorded?",
            "option_a": "At the exchange rate on the transaction date",
            "option_b": "At the exchange rate on the reporting date",
            "option_c": "At the average exchange rate for the period",
            "option_d": "At the exchange rate when cash is received",
            "correct_answer": "a",
            "explanation": "Foreign currency transactions should be initially recorded at the exchange rate prevailing on the transaction date.",
            "category": "Foreign Currency Transactions"
        }
    ]
    
    try:
        for question in sample_questions:
            supabase.table('questions').insert(question).execute()
        st.success("Sample questions seeded successfully!")
    except Exception as e:
        st.error(f"Error seeding questions: {e}")

def get_questions(supabase: Client, category=None):
    """Get questions from the database"""
    try:
        if category:
            response = supabase.table('questions').select('*').eq('category', category).execute()
        else:
            response = supabase.table('questions').select('*').execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching questions: {e}")
        return []

def save_quiz_result(supabase: Client, user_id, quiz_data, score, answers):
    """Save quiz results to the database"""
    try:
        result = {
            "user_id": user_id,
            "quiz_data": quiz_data,
            "score": score,
            "answers": answers,
            "completed_at": datetime.now().isoformat()
        }
        supabase.table('quiz_results').insert(result).execute()
    except Exception as e:
        st.error(f"Error saving quiz result: {e}")

# Authentication functions
def sign_up(supabase: Client, email, password):
    """Sign up a new user"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        st.error(f"Error during sign up: {e}")
        return None

def sign_in(supabase: Client, email, password):
    """Sign in an existing user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        st.error(f"Error during sign in: {e}")
        return None

def sign_out(supabase: Client):
    """Sign out the current user"""
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.current_quiz = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_completed = False
        st.rerun()
    except Exception as e:
        st.error(f"Error during sign out: {e}")

# Quiz functions
def start_quiz(questions, time_limit_minutes=15):
    """Start a new quiz session"""
    st.session_state.current_quiz = {
        "questions": questions,
        "time_limit": time_limit_minutes,
        "start_time": datetime.now()
    }
    st.session_state.quiz_start_time = time.time()
    st.session_state.quiz_answers = {}
    st.session_state.quiz_completed = False

def calculate_score(questions, answers):
    """Calculate quiz score"""
    if not answers:
        return 0
    
    correct = 0
    total = len(questions)
    
    for question in questions:
        question_id = str(question['id'])
        if question_id in answers:
            if answers[question_id] == question['correct_answer']:
                correct += 1
    
    return (correct / total) * 100 if total > 0 else 0

def display_quiz_timer():
    """Display countdown timer for the quiz"""
    if st.session_state.quiz_start_time and st.session_state.current_quiz:
        elapsed = time.time() - st.session_state.quiz_start_time
        time_limit = st.session_state.current_quiz['time_limit'] * 60
        remaining = max(0, time_limit - elapsed)
        
        if remaining <= 0:
            st.error("Time's up! Quiz will be submitted automatically.")
            submit_quiz()
            return False
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.metric("Time Remaining", f"{minutes:02d}:{seconds:02d}")
        
        return True
    return False

def submit_quiz():
    """Submit the quiz and show results"""
    if not st.session_state.current_quiz or not st.session_state.quiz_answers:
        st.warning("No quiz to submit!")
        return
    
    questions = st.session_state.current_quiz['questions']
    score = calculate_score(questions, st.session_state.quiz_answers)
    
    # Save results
    supabase = init_supabase()
    if st.session_state.user:
        save_quiz_result(
            supabase, 
            st.session_state.user.id, 
            st.session_state.current_quiz, 
            score, 
            st.session_state.quiz_answers
        )
    
    # Display results
    st.session_state.quiz_completed = True
    st.success(f"Quiz completed! Your score: {score:.1f}%")
    
    # Show detailed results
    st.subheader("Quiz Results")
    
    for i, question in enumerate(questions):
        question_id = str(question['id'])
        user_answer = st.session_state.quiz_answers.get(question_id, 'No answer')
        correct_answer = question['correct_answer']
        is_correct = user_answer == correct_answer
        
        with st.expander(f"Question {i+1}: {question['question']}"):
            st.write(f"**Your answer:** {user_answer.upper()}")
            st.write(f"**Correct answer:** {correct_answer.upper()}")
            st.write(f"**Explanation:** {question['explanation']}")
            
            if is_correct:
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect!")

# Main application
def main():
    st.title("🧠 Accounting Quiz App")
    
    # Initialize Supabase
    supabase = init_supabase()
    
    # Sidebar for authentication
    with st.sidebar:
        st.header("Authentication")
        
        if st.session_state.user is None:
            # Login/Signup form
            tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
            
            with tab1:
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Sign In"):
                    if email and password:
                        response = sign_in(supabase, email, password)
                        if response and response.user:
                            st.session_state.user = response.user
                            st.rerun()
                    else:
                        st.warning("Please enter both email and password")
            
            with tab2:
                new_email = st.text_input("Email", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                
                if st.button("Sign Up"):
                    if new_email and new_password and new_password == confirm_password:
                        response = sign_up(supabase, new_email, new_password)
                        if response:
                            st.success("Account created successfully! Please sign in.")
                    else:
                        st.warning("Please fill all fields and ensure passwords match")
        
        else:
            # User is logged in
            st.success(f"Welcome, {st.session_state.user.email}!")
            
            if st.button("Sign Out"):
                sign_out(supabase)
            
            # Admin section
            if st.session_state.user.email == os.getenv("ADMIN_EMAIL", "admin@example.com"):
                # Import and render enhanced admin panel
                from admin_panel import render_admin_panel
                render_admin_panel(supabase, st.session_state.user.email)
    
    # Main content area
    if st.session_state.user is None:
        st.info("Please sign in to access the quiz app.")
        return
    
    # Quiz selection
    if not st.session_state.current_quiz:
        st.header("Select a Quiz")
        
        # Get available categories
        questions = get_questions(supabase)
        categories = list(set([q['category'] for q in questions])) if questions else []
        
        if not categories:
            st.warning("No quizzes available. Please contact an administrator.")
            return
        
        selected_category = st.selectbox("Choose a quiz category:", categories)
        
        if st.button("Start Quiz"):
            category_questions = get_questions(supabase, selected_category)
            if category_questions:
                start_quiz(category_questions)
                st.rerun()
            else:
                st.error("No questions found for this category.")
    
    # Quiz taking interface
    elif st.session_state.current_quiz and not st.session_state.quiz_completed:
        st.header("Quiz in Progress")
        
        # Display timer
        if not display_quiz_timer():
            return
        
        # Quiz questions
        questions = st.session_state.current_quiz['questions']
        
        for i, question in enumerate(questions):
            st.subheader(f"Question {i+1}")
            st.write(question['question'])
            
            options = {
                'a': question['option_a'],
                'b': question['option_b'],
                'c': question['option_c'],
                'd': question['option_d']
            }
            
            question_id = str(question['id'])
            answer = st.radio(
                "Select your answer:",
                options=list(options.keys()),
                format_func=lambda x: f"{x.upper()}. {options[x]}",
                key=f"q_{question_id}"
            )
            
            st.session_state.quiz_answers[question_id] = answer
        
        # Submit button
        if st.button("Submit Quiz"):
            submit_quiz()
            st.rerun()
    
    # Quiz results
    elif st.session_state.quiz_completed:
        st.header("Quiz Results")
        
        if st.button("Take Another Quiz"):
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_completed = False
            st.rerun()

if __name__ == "__main__":
    main()
