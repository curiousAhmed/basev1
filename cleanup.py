import os
import shutil
import fileinput
import re

# Modules to remove (update this list)
MODULES_TO_REMOVE = [
    "recruitment",
    "pms",
    "onboarding",
    "asset",
    # "base",  # Uncomment if safe to remove
]

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(PROJECT_ROOT, "friday", "settings.py")
URLS_PATH = os.path.join(PROJECT_ROOT, "friday", "urls.py")

def remove_installed_apps():
    """Remove modules from INSTALLED_APPS in settings.py"""
    with fileinput.FileInput(SETTINGS_PATH, inplace=True) as file:
        for line in file:
            if not any(module in line for module in MODULES_TO_REMOVE):
                print(line, end='')

def remove_url_routes():
    """Remove URL routes linked to deleted modules"""
    with fileinput.FileInput(URLS_PATH, inplace=True) as file:
        for line in file:
            if not any(f"'{module}" in line or f'"{module}"' in line for module in MODULES_TO_REMOVE):
                print(line, end='')

def delete_app_directories():
    """Delete app directories"""
    for module in MODULES_TO_REMOVE:
        module_path = os.path.join(PROJECT_ROOT, module)
        if os.path.exists(module_path):
            shutil.rmtree(module_path)
            print(f"Deleted: {module_path}")

def cleanup_imports():
    """Remove unused imports in .py files"""
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if not file.endswith(".py"):
                continue  # Skip non-Python files
            file_path = os.path.join(root, file)
            try:
                # Read and rewrite the file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding='utf-8') as f:
                    for line in lines:
                        if not any(
                            f"from {module}" in line or 
                            f"import {module}" in line 
                            for module in MODULES_TO_REMOVE
                        ):
                            f.write(line)
            except UnicodeDecodeError:
                # Skip files with invalid encoding
                print(f"Skipping {file_path} due to encoding issues")
                continue
            except Exception as e:
                # Handle other unexpected errors
                print(f"Error processing {file_path}: {e}")
                continue

if __name__ == "__main__":
    # 1. Remove from INSTALLED_APPS
    remove_installed_apps()
    
    # 2. Remove URL routes
    remove_url_routes()
    
    # 3. Delete app directories
    delete_app_directories()
    
    # 4. Clean up imports
    cleanup_imports()
    
    print("Cleanup complete. Run migrations now:")
    print("python manage.py makemigrations && python manage.py migrate")