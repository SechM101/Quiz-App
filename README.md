# 🧠 Accounting Quiz App

A comprehensive quiz application built with **Streamlit** and **Supabase** for testing accounting knowledge. The app features user authentication, timed quizzes, progress tracking, and an admin panel for quiz management.

## ✨ Features

### 🔐 User Authentication & Tracking
- Secure user registration and login via Supabase Auth
- Individual user progress tracking
- Quiz results tied to user accounts

### ⏱️ Quiz Timer
- Configurable countdown timer for each quiz
- Automatic quiz submission when time expires
- Real-time countdown display

### 📚 Quiz Management
- **Admin Panel**: Add, edit, and delete quiz questions
- **User Interface**: Take quizzes with multiple-choice questions
- **Categories**: Organized quiz topics (IFRS 15, Xero, Matching Concept, etc.)

### 📊 Quiz Flow & Results
- Multiple-choice question format
- Immediate feedback after quiz completion
- Detailed score breakdown with explanations
- Question-by-question review with correct answers

### 🎯 Sample Content
- **IFRS 15**: Revenue recognition principles
- **Xero & Accounting Standards**: Prepayment and deferred revenue scenarios
- **Matching Concept**: Expense-revenue matching principles
- **Foreign Currency Transactions**: Exchange rate recording

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account and project
- Git (optional)

### 1. Clone/Download the Project
```bash
# If using Git
git clone <repository-url>
cd quiz_app

# Or download and extract the ZIP file
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase

#### A. Create a Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

#### B. Set Up Database
1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Copy and paste the contents of `database_setup.sql`
4. Run the script to create tables and sample data

#### C. Configure Authentication
1. In Supabase dashboard, go to **Authentication > Settings**
2. Enable **Email confirmations** (optional but recommended)
3. Configure any additional auth providers as needed

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
ADMIN_EMAIL=your_admin_email@example.com
```

**Important**: Replace the placeholder values with your actual Supabase credentials.

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🏗️ Project Structure

```
quiz_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── database_setup.sql    # Database schema and sample data
├── README.md             # This file
└── .env                  # Environment variables (create this)
```

## 🔧 Configuration

### Admin Access
- Set your email in the `.env` file as `ADMIN_EMAIL`
- Admin users can:
  - Seed sample questions
  - Create/edit/delete quiz questions
  - Access admin panel features

### Quiz Timer
- Default timer: 15 minutes per quiz
- Modify in `start_quiz()` function in `app.py`
- Timer automatically submits quiz when expired

### Database Schema
The app uses two main tables:
- **`questions`**: Stores quiz questions, options, and correct answers
- **`quiz_results`**: Tracks user quiz attempts and scores

## 📱 Usage Guide

### For Users
1. **Sign Up/Login**: Use the sidebar authentication form
2. **Select Quiz**: Choose from available quiz categories
3. **Take Quiz**: Answer questions within the time limit
4. **View Results**: See your score and review answers
5. **Track Progress**: All results are saved to your account

### For Admins
1. **Access Admin Panel**: Available in sidebar when logged in as admin
2. **Seed Questions**: Add sample questions to the database
3. **Manage Content**: Add, edit, or remove quiz questions
4. **Monitor Usage**: View quiz results and user activity

## 🛡️ Security Features

- **Row Level Security (RLS)**: Users can only access their own data
- **Authentication**: Secure user registration and login
- **Admin Controls**: Restricted access to quiz management features
- **Input Validation**: Server-side validation of all user inputs

## 🔍 Troubleshooting

### Common Issues

#### "Missing Supabase credentials"
- Ensure `.env` file exists and contains correct credentials
- Check that `SUPABASE_URL` and `SUPABASE_KEY` are set correctly

#### "Table doesn't exist"
- Run the `database_setup.sql` script in Supabase SQL Editor
- Check that all tables were created successfully

#### "Authentication errors"
- Verify Supabase Auth is properly configured
- Check email confirmation settings if enabled

#### "Permission denied"
- Ensure RLS policies are correctly set up
- Verify user authentication status

### Getting Help
1. Check the Supabase dashboard for error logs
2. Verify database schema matches the setup script
3. Ensure all environment variables are correctly set
4. Check Python dependencies are properly installed

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Deploy directly from GitHub
2. **Heroku**: Use the Streamlit buildpack
3. **Docker**: Containerize the application
4. **VPS**: Traditional server deployment

### Environment Variables for Production
- Set production Supabase credentials
- Configure admin email for production
- Enable HTTPS and secure cookies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review Supabase documentation
- Open an issue in the repository

---

**Built with ❤️ using Streamlit and Supabase**
