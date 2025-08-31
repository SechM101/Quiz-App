"""
Configuration file for the Quiz App
Centralizes all configurable settings
"""

import os
from typing import Dict, Any

class Config:
    """Application configuration class"""
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Admin Configuration
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    
    # Quiz Configuration
    DEFAULT_QUIZ_TIME_MINUTES = 15
    MAX_QUESTIONS_PER_QUIZ = 50
    
    # UI Configuration
    PAGE_TITLE = "🧠 Accounting Quiz App"
    PAGE_ICON = "🧠"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Database Configuration
    TABLES = {
        "questions": "questions",
        "quiz_results": "quiz_results"
    }
    
    # Quiz Categories
    DEFAULT_CATEGORIES = [
        "IFRS 15",
        "Xero and Accounting Standards", 
        "Matching Concept",
        "Foreign Currency Transactions"
    ]
    
    # Sample Questions (can be overridden)
    SAMPLE_QUESTIONS = [
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
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration and return any issues"""
        issues = []
        
        if not cls.SUPABASE_URL:
            issues.append("SUPABASE_URL is not set")
        
        if not cls.SUPABASE_KEY:
            issues.append("SUPABASE_KEY is not set")
        
        if not cls.ADMIN_EMAIL:
            issues.append("ADMIN_EMAIL is not set")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    @classmethod
    def get_supabase_config(cls) -> Dict[str, str]:
        """Get Supabase configuration"""
        return {
            "url": cls.SUPABASE_URL,
            "key": cls.SUPABASE_KEY
        }
    
    @classmethod
    def is_admin(cls, email: str) -> bool:
        """Check if a user is an admin"""
        return email == cls.ADMIN_EMAIL

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    
    # Override for production
    DEFAULT_QUIZ_TIME_MINUTES = 20

# Configuration factory
def get_config(environment: str = None) -> Config:
    """Get configuration based on environment"""
    if not environment:
        environment = os.getenv("ENVIRONMENT", "development")
    
    if environment.lower() == "production":
        return ProductionConfig()
    
    return DevelopmentConfig()

# Default configuration instance
config = get_config()
