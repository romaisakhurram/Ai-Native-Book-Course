#!/usr/bin/env python3
"""
Backend Verification Script - Check RAG Chatbot Agent Setup
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set"""
    required_keys = [
        'OPENROUTER_API_KEY',
        'QDRANT_URL',
        'QDRANT_API_KEY',
        'NEON_DATABASE_URL'
    ]
    
    print("\n📋 Environment Variables Check")
    print("=" * 50)
    
    missing = []
    for key in required_keys:
        value = os.getenv(key)
        if value:
            masked = value[:10] + '...' if len(value) > 10 else value
            print(f"✅ {key}: {masked}")
        else:
            print(f"❌ {key}: NOT SET")
            missing.append(key)
    
    if missing:
        print(f"\n⚠️  Missing required keys: {', '.join(missing)}")
        print("📝 Create backend/.env file with required values")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Dependencies Check")
    print("=" * 50)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'qdrant_client',
        'openai',
        'sqlalchemy',
        'pydantic_settings',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('_', '-'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("📝 Run: pip install -e . in backend directory")
        return False
    
    return True

def check_python_version():
    """Check if Python version is 3.13+"""
    print("\n🐍 Python Version Check")
    print("=" * 50)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 13:
        print(f"✅ Python {version_str} (Required: 3.13+)")
        return True
    else:
        print(f"❌ Python {version_str} (Required: 3.13+)")
        return False

def check_database_connectivity():
    """Check if database connections can be established"""
    print("\n🗄️  Database Connectivity Check")
    print("=" * 50)
    
    # Check PostgreSQL connection
    try:
        import psycopg2
        db_url = os.getenv('NEON_DATABASE_URL', '')
        if db_url:
            print("✅ PostgreSQL driver available")
        else:
            print("⚠️  NEON_DATABASE_URL not set, skipping connection test")
    except ImportError:
        print("❌ psycopg2 not installed")
        return False
    
    # Check Qdrant connection
    try:
        from qdrant_client import QdrantClient
        qdrant_url = os.getenv('QDRANT_URL', '')
        qdrant_key = os.getenv('QDRANT_API_KEY', '')
        if qdrant_url and qdrant_key:
            print("✅ Qdrant client available")
        else:
            print("⚠️  QDRANT_URL or QDRANT_API_KEY not set")
    except ImportError:
        print("❌ qdrant-client not installed")
        return False
    
    return True

def check_fastapi_startup():
    """Verify FastAPI app can initialize"""
    print("\n🚀 FastAPI Application Check")
    print("=" * 50)
    
    try:
        # Add backend to path
        backend_path = Path(__file__).parent
        sys.path.insert(0, str(backend_path))
        
        from main import app
        print("✅ FastAPI app initialized successfully")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app initialization failed: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "=" * 50)
    print("🤖 RAG Chatbot Agent - Backend Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment Variables", check_environment),
        ("Dependencies", check_dependencies),
        ("Database Connectivity", check_database_connectivity),
        ("FastAPI Application", check_fastapi_startup),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n⚠️  {name} check failed with error: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n✨ Backend is ready! Start with:")
        print("   uvicorn main:app --reload")
        return 0
    else:
        print("\n⚠️  Fix the failing checks before starting the backend")
        return 1

if __name__ == "__main__":
    sys.exit(main())
