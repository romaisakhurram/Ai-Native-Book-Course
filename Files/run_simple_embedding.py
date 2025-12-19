"""
Simple script to run the embedding process
"""
import sys
import os
from pathlib import Path

# Add the project root and backend to the path so we can import our modules
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_path))

def run_embedding():
    # Import required modules after setting up the path
    from scripts.index_book_content import main
    
    # Set command-line arguments
    import sys
    sys.argv = ['index_book_content.py', '--source-path', 'frontend/docs']
    
    # Run the main function
    main()

if __name__ == "__main__":
    run_embedding()