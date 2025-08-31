# 🚀 Quick Setup Guide

Follow these steps to get your Quiz App running in minutes!

## 📋 Prerequisites

- Python 3.8 or higher
- A Supabase account (free at [supabase.com](https://supabase.com))

## ⚡ Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
Create a `.env` file in the project root with your Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
ADMIN_EMAIL=your-email@example.com
```

**How to get these values:**
1. Go to [supabase.com](https://supabase.com) and create a new project
2. In your project dashboard, go to **Settings > API**
3. Copy the **Project URL** and **anon public** key
4. Set your email as the admin email

### 3. Set Up Database
1. In your Supabase dashboard, go to **SQL Editor**
2. Copy the entire contents of `database_setup.sql`
3. Paste and run the script
4. This creates all necessary tables and sample questions

### 4. Run the App
```bash
streamlit run app.py
```

Or on Windows, double-click `run_app.bat`

The app will open at `http://localhost:8501`

## 🔧 Detailed Setup

### Supabase Project Setup

1. **Create Project**
   - Visit [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose organization and enter project name
   - Set database password (save this!)
   - Choose region close to your users
   - Wait for setup to complete (2-3 minutes)

2. **Get API Keys**
   - Go to **Settings > API** in your project
   - Copy **Project URL** and **anon public** key
   - These go in your `.env` file

3. **Database Setup**
   - Go to **SQL Editor** in your project
   - Copy contents of `database_setup.sql`
   - Paste and run the script
   - Verify tables are created in **Table Editor**

4. **Authentication Setup**
   - Go to **Authentication > Settings**
   - Enable **Email confirmations** (recommended)
   - Set **Site URL** to `http://localhost:8501` for development

### Local Development

1. **Clone/Download Project**
   ```bash
   # If using Git
   git clone <repository-url>
   cd quiz_app
   
   # Or download and extract ZIP
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Environment File**
   ```bash
   # Windows
   copy .env.example .env
   
   # Then edit .env with your credentials
   ```

4. **Test Setup**
   ```bash
   python test_setup.py
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

## 🧪 Testing Your Setup

Run the test script to verify everything is working:

```bash
python test_setup.py
```

This will check:
- ✅ Environment variables
- ✅ Dependencies
- ✅ Configuration
- ✅ Supabase connection

## 🚨 Common Issues & Solutions

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Missing Supabase credentials"
- Check your `.env` file exists
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Restart your terminal after creating `.env`

### "Table doesn't exist"
- Run `database_setup.sql` in Supabase SQL Editor
- Check the script executed without errors

### "Permission denied"
- Verify RLS policies are set up correctly
- Check user authentication status

### "Connection failed"
- Verify Supabase project is active
- Check URL and key are correct
- Ensure no firewall blocking connections

## 📱 First Run

1. **Open the app** in your browser
2. **Sign up** with your admin email
3. **Sign in** to access the admin panel
4. **Seed sample questions** using the admin panel
5. **Take a test quiz** to verify everything works

## 🔐 Admin Access

- Set your email as `ADMIN_EMAIL` in `.env`
- Admin users can:
  - Add/edit/delete questions
  - View all quiz results
  - Access statistics dashboard
  - Seed sample content

## 🚀 Next Steps

- **Customize Questions**: Add your own accounting questions
- **Branding**: Update app title and styling
- **Deploy**: Use Streamlit Cloud for production
- **Integrate**: Connect with other systems

## 📞 Need Help?

1. Check the troubleshooting section in `README.md`
2. Verify your setup with `python test_setup.py`
3. Check Supabase dashboard for error logs
4. Review the code comments for guidance

---

**Happy Quizzing! 🎉**
