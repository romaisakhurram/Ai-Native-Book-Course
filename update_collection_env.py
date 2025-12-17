"""
Script to update the collection name in the .env file
"""
import os
import re
from pathlib import Path

def update_collection_name(new_collection_name: str):
    """
    Updates the QDRANT_COLLECTION_NAME in the .env file
    :param new_collection_name: The new collection name to set
    """
    # Define the path to the .env file
    env_path = Path(__file__).parent / "backend" / ".env"
    
    # Check if the .env file exists
    if not env_path.exists():
        print(f"❌ .env file not found at: {env_path}")
        return False
    
    print(f"Current .env file path: {env_path}")
    
    # Read the current content of the .env file
    with open(env_path, 'r') as file:
        content = file.read()
    
    print(f"Current collection name in .env file:")
    collection_match = re.search(r'QDRANT_COLLECTION_NAME=(.*)', content)
    if collection_match:
        current_name = collection_match.group(1).strip('"\'')  # Remove quotes if present
        print(f"   Current: {current_name}")
    else:
        print("   Current: Not found")
        current_name = ""
    
    print(f"Changing to: {new_collection_name}")
    
    # Replace or add the QDRANT_COLLECTION_NAME
    if collection_match:
        # Replace the existing line
        updated_content = re.sub(
            r'QDRANT_COLLECTION_NAME=.*',
            f'QDRANT_COLLECTION_NAME="{new_collection_name}"',
            content
        )
    else:
        # Add the line if it doesn't exist
        updated_content = content + f'\nQDRANT_COLLECTION_NAME="{new_collection_name}"\n'
    
    # Write the updated content back to the file
    with open(env_path, 'w') as file:
        file.write(updated_content)
    
    print(f"✅ Successfully updated QDRANT_COLLECTION_NAME to: {new_collection_name}")
    
    # Verify the change
    with open(env_path, 'r') as file:
        new_content = file.read()
    
    verify_match = re.search(r'QDRANT_COLLECTION_NAME=(.*)', new_content)
    if verify_match:
        verified_name = verify_match.group(1).strip('"\'')
        if verified_name == new_collection_name:
            print(f"✅ Verification successful: Collection name is now {verified_name}")
            return True
        else:
            print(f"❌ Verification failed: Expected {new_collection_name}, got {verified_name}")
            return False
    else:
        print(f"❌ Could not verify the change")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Update QDRANT_COLLECTION_NAME in .env file')
    parser.add_argument('--name', required=True, help='New collection name to set in .env')
    
    args = parser.parse_args()
    
    success = update_collection_name(args.name)
    
    if success:
        print(f"\n🎉 Successfully updated collection name to: {args.name}")
        print(f"📖 The embedding service will now use '{args.name}' as the collection")
    else:
        print(f"\n❌ Failed to update collection name")
        exit(1)

if __name__ == "__main__":
    main()