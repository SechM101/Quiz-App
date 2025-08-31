#!/usr/bin/env python3
"""
Test script to verify Quiz App setup
Run this to check if everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables and configuration"""
    print("🔍 Testing Environment Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'ADMIN_EMAIL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)} (length: {len(value)})")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are set")
    return True

def test_dependencies():
    """Test if required packages can be imported"""
    print("\n📦 Testing Dependencies...")
    
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import supabase
        print(f"✅ Supabase: {supabase.__version__}")
    except ImportError as e:
        print(f"❌ Supabase import failed: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas: {pandas.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import dotenv
        print(f"✅ Python-dotenv: {dotenv.__version__}")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    print("✅ All dependencies are available")
    return True

def test_configuration():
    """Test configuration file"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from config import config
        print("✅ Configuration file loaded successfully")
        
        # Test config validation
        validation = config.validate()
        if validation['valid']:
            print("✅ Configuration validation passed")
        else:
            print(f"❌ Configuration validation failed: {validation['issues']}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    return True

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔌 Testing Supabase Connection...")
    
    try:
        from supabase import create_client
        from config import config
        
        supabase = create_client(
            config.SUPABASE_URL,
            config.SUPABASE_KEY
        )
        
        # Try a simple query to test connection
        response = supabase.table('questions').select('id').limit(1).execute()
        print("✅ Supabase connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("💡 Make sure your Supabase project is running and credentials are correct")
        return False

def main():
    """Run all tests"""
    print("🧠 Quiz App Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment),
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Supabase Connection", test_supabase_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Quiz App is ready to run.")
        print("\nTo start the app, run:")
        print("  streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the app.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
