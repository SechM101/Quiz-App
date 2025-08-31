import streamlit as st
from supabase import Client
from typing import List, Dict, Any
import pandas as pd

def render_admin_panel(supabase: Client, user_email: str):
    """Render the admin panel with quiz management features"""
    
    st.header("🔧 Admin Panel")
    st.info(f"Logged in as: {user_email}")
    
    # Admin actions tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 View Questions", 
        "➕ Add Question", 
        "✏️ Edit Question", 
        "🗑️ Delete Question"
    ])
    
    with tab1:
        render_view_questions(supabase)
    
    with tab2:
        render_add_question(supabase)
    
    with tab3:
        render_edit_question(supabase)
    
    with tab4:
        render_delete_question(supabase)

def render_view_questions(supabase: Client):
    """Display all questions in a table format"""
    st.subheader("📋 All Quiz Questions")
    
    try:
        # Fetch all questions
        response = supabase.table('questions').select('*').order('category', 'created_at').execute()
        questions = response.data
        
        if not questions:
            st.warning("No questions found in the database.")
            return
        
        # Convert to DataFrame for better display
        df_data = []
        for q in questions:
            df_data.append({
                'ID': q['id'],
                'Question': q['question'][:100] + '...' if len(q['question']) > 100 else q['question'],
                'Category': q['category'],
                'Correct Answer': q['correct_answer'].upper(),
                'Created': q['created_at'][:10] if q['created_at'] else 'N/A'
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Show question count by category
        st.subheader("📈 Question Statistics")
        category_counts = df['Category'].value_counts()
        st.bar_chart(category_counts)
        
    except Exception as e:
        st.error(f"Error fetching questions: {e}")

def render_add_question(supabase: Client):
    """Form to add a new question"""
    st.subheader("➕ Add New Question")
    
    with st.form("add_question_form"):
        # Question details
        question = st.text_area("Question Text", height=100, placeholder="Enter your question here...")
        
        # Options
        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Option A", placeholder="First option")
            option_c = st.text_input("Option C", placeholder="Third option")
        
        with col2:
            option_b = st.text_input("Option B", placeholder="Second option")
            option_d = st.text_input("Option D", placeholder="Fourth option")
        
        # Correct answer and category
        correct_answer = st.selectbox("Correct Answer", ['a', 'b', 'c', 'd'])
        explanation = st.text_area("Explanation", height=80, placeholder="Explain why this answer is correct...")
        category = st.text_input("Category", placeholder="e.g., IFRS 15, Xero, etc.")
        
        submitted = st.form_submit_button("Add Question")
        
        if submitted:
            if validate_question_form(question, option_a, option_b, option_c, option_d, explanation, category):
                try:
                    new_question = {
                        "question": question,
                        "option_a": option_a,
                        "option_b": option_b,
                        "option_c": option_c,
                        "option_d": option_d,
                        "correct_answer": correct_answer,
                        "explanation": explanation,
                        "category": category
                    }
                    
                    response = supabase.table('questions').insert(new_question).execute()
                    
                    if response.data:
                        st.success("✅ Question added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add question.")
                        
                except Exception as e:
                    st.error(f"Error adding question: {e}")

def render_edit_question(supabase: Client):
    """Form to edit existing questions"""
    st.subheader("✏️ Edit Question")
    
    try:
        # Fetch questions for selection
        response = supabase.table('questions').select('id, question, category').execute()
        questions = response.data
        
        if not questions:
            st.warning("No questions available to edit.")
            return
        
        # Question selector
        question_options = {f"{q['question'][:50]}... ({q['category']})": q['id'] for q in questions}
        selected_question_text = st.selectbox("Select Question to Edit", list(question_options.keys()))
        
        if selected_question_text:
            question_id = question_options[selected_question_text]
            
            # Fetch full question data
            question_response = supabase.table('questions').select('*').eq('id', question_id).execute()
            if question_response.data:
                question_data = question_response.data[0]
                
                with st.form("edit_question_form"):
                    st.write(f"**Editing Question ID:** {question_id}")
                    
                    # Editable fields
                    question = st.text_area("Question Text", value=question_data['question'], height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        option_a = st.text_input("Option A", value=question_data['option_a'])
                        option_c = st.text_input("Option C", value=question_data['option_c'])
                    
                    with col2:
                        option_b = st.text_input("Option B", value=question_data['option_b'])
                        option_d = st.text_input("Option D", value=question_data['option_d'])
                    
                    correct_answer = st.selectbox("Correct Answer", ['a', 'b', 'c', 'd'], index=['a', 'b', 'c', 'd'].index(question_data['correct_answer']))
                    explanation = st.text_area("Explanation", value=question_data['explanation'], height=80)
                    category = st.text_input("Category", value=question_data['category'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Question"):
                            if validate_question_form(question, option_a, option_b, option_c, option_d, explanation, category):
                                try:
                                    updated_question = {
                                        "question": question,
                                        "option_a": option_a,
                                        "option_b": option_b,
                                        "option_c": option_c,
                                        "option_d": option_d,
                                        "correct_answer": correct_answer,
                                        "explanation": explanation,
                                        "category": category
                                    }
                                    
                                    response = supabase.table('questions').update(updated_question).eq('id', question_id).execute()
                                    
                                    if response.data:
                                        st.success("✅ Question updated successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update question.")
                                        
                                except Exception as e:
                                    st.error(f"Error updating question: {e}")
                    
                    with col2:
                        if st.form_submit_button("Cancel", type="secondary"):
                            st.rerun()
    
    except Exception as e:
        st.error(f"Error loading questions for editing: {e}")

def render_delete_question(supabase: Client):
    """Interface to delete questions"""
    st.subheader("🗑️ Delete Question")
    
    try:
        # Fetch questions for selection
        response = supabase.table('questions').select('id, question, category').execute()
        questions = response.data
        
        if not questions:
            st.warning("No questions available to delete.")
            return
        
        # Question selector
        question_options = {f"{q['question'][:50]}... ({q['category']})": q['id'] for q in questions}
        selected_question_text = st.selectbox("Select Question to Delete", list(question_options.keys()))
        
        if selected_question_text:
            question_id = question_options[selected_question_text]
            
            # Show question details
            question_response = supabase.table('questions').select('*').eq('id', question_id).execute()
            if question_response.data:
                question_data = question_response.data[0]
                
                st.warning("⚠️ **Question Details**")
                st.write(f"**Question:** {question_data['question']}")
                st.write(f"**Category:** {question_data['category']}")
                st.write(f"**Correct Answer:** {question_data['correct_answer'].upper()}")
                
                # Confirmation
                if st.button("🗑️ Delete This Question", type="primary"):
                    try:
                        response = supabase.table('questions').delete().eq('id', question_id).execute()
                        
                        if response.data:
                            st.success("✅ Question deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete question.")
                            
                    except Exception as e:
                        st.error(f"Error deleting question: {e}")
    
    except Exception as e:
        st.error(f"Error loading questions for deletion: {e}")

def validate_question_form(question: str, option_a: str, option_b: str, option_c: str, option_d: str, explanation: str, category: str) -> bool:
    """Validate the question form data"""
    errors = []
    
    if not question.strip():
        errors.append("Question text is required")
    
    if not option_a.strip() or not option_b.strip() or not option_c.strip() or not option_d.strip():
        errors.append("All options (A, B, C, D) are required")
    
    if not explanation.strip():
        errors.append("Explanation is required")
    
    if not category.strip():
        errors.append("Category is required")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return False
    
    return True

def get_quiz_statistics(supabase: Client) -> Dict[str, Any]:
    """Get comprehensive quiz statistics"""
    try:
        # Question statistics
        questions_response = supabase.table('questions').select('category').execute()
        questions = questions_response.data
        
        # Quiz results statistics
        results_response = supabase.table('quiz_results').select('score, completed_at').execute()
        results = results_response.data
        
        stats = {
            'total_questions': len(questions),
            'categories': list(set([q['category'] for q in questions])),
            'total_quizzes_taken': len(results),
            'average_score': sum([r['score'] for r in results]) / len(results) if results else 0,
            'recent_activity': len([r for r in results if r['completed_at'] > '2024-01-01'])
        }
        
        return stats
        
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
        return {}

def render_statistics_dashboard(supabase: Client):
    """Render a statistics dashboard for admins"""
    st.subheader("📊 Statistics Dashboard")
    
    stats = get_quiz_statistics(supabase)
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", stats['total_questions'])
        
        with col2:
            st.metric("Categories", len(stats['categories']))
        
        with col3:
            st.metric("Quizzes Taken", stats['total_quizzes_taken'])
        
        with col4:
            st.metric("Avg Score", f"{stats['average_score']:.1f}%")
        
        # Category breakdown
        if stats['categories']:
            st.subheader("📈 Questions by Category")
            category_counts = {}
            for category in stats['categories']:
                category_response = supabase.table('questions').select('id').eq('category', category).execute()
                category_counts[category] = len(category_response.data)
            
            st.bar_chart(pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count']))
