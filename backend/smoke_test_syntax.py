#!/usr/bin/env python3
"""
Smoke Test: Backend - Syntax & Structure Check
Minimal smoke test that runs without any dependencies

This test verifies:
1. All Python files have valid syntax
2. Directory structure is correct
3. Required files exist
"""
import sys
import os
import py_compile

def main():
    print("=" * 60)
    print("🔥 SMOKE TEST: Backend Syntax & Structure")
    print("=" * 60)

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    errors = []

    try:
        # Test 1: Directory structure
        print("\n[1/4] Checking directory structure...")
        required_dirs = [
            "models",
            "services",
            "api",
            "tests",
            "tests/unit",
            "tests/integration"
        ]
        for dir_name in required_dirs:
            dir_path = os.path.join(backend_dir, dir_name)
            if not os.path.isdir(dir_path):
                errors.append(f"Missing directory: {dir_name}")
            else:
                print(f"      ✅ {dir_name}/")

        if errors:
            raise AssertionError(f"Directory structure errors: {errors}")

        print(f"      ✅ Directory structure OK")

        # Test 2: Required files exist
        print("\n[2/4] Checking required files...")
        required_files = [
            "main.py",
            "requirements.txt",
            "models/__init__.py",
            "models/schemas.py",
            "models/constants.py",
            "services/__init__.py",
            "services/calculation_service.py",
            "services/validation_service.py",
            "tests/conftest.py",
        ]
        for file_name in required_files:
            file_path = os.path.join(backend_dir, file_name)
            if not os.path.isfile(file_path):
                errors.append(f"Missing file: {file_name}")

        if errors:
            raise AssertionError(f"Missing files: {errors}")

        print(f"      ✅ All required files exist ({len(required_files)} files)")

        # Test 3: Syntax check all Python files
        print("\n[3/4] Checking Python syntax...")
        python_files = []
        for root, dirs, files in os.walk(backend_dir):
            # Skip __pycache__ and venv directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.pytest_cache']]

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, backend_dir)
                    python_files.append(file_path)

                    try:
                        py_compile.compile(file_path, doraise=True)
                    except py_compile.PyCompileError as e:
                        errors.append(f"Syntax error in {rel_path}: {e}")

        if errors:
            raise AssertionError(f"Syntax errors: {errors}")

        print(f"      ✅ Syntax OK ({len(python_files)} Python files)")

        # Test 4: Check requirements.txt
        print("\n[4/4] Checking requirements.txt...")
        req_path = os.path.join(backend_dir, "requirements.txt")
        with open(req_path) as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        required_packages = ['fastapi', 'uvicorn', 'pydantic', 'pytest']
        missing_packages = []
        for pkg in required_packages:
            if not any(pkg in req for req in requirements):
                missing_packages.append(pkg)

        if missing_packages:
            errors.append(f"Missing packages in requirements.txt: {missing_packages}")

        if errors:
            raise AssertionError(f"Requirements errors: {errors}")

        print(f"      ✅ Requirements OK ({len(requirements)} packages)")

        print("\n" + "=" * 60)
        print("🎉 SMOKE TEST PASSED!")
        print("=" * 60)
        print("\n✅ All 4 checks successful:")
        print("   1. Directory structure correct")
        print(f"   2. All required files exist ({len(required_files)} files)")
        print(f"   3. Python syntax valid ({len(python_files)} files)")
        print(f"   4. Requirements complete ({len(requirements)} packages)")
        print("\n✅ Backend structure verified!")
        print("\n" + "=" * 60)
        print("📝 NEXT STEPS FOR FULL TESTING:")
        print("=" * 60)
        print("\n1. Create virtual environment:")
        print("   python3.12 -m venv backend/venv")
        print("   source backend/venv/bin/activate")
        print("")
        print("2. Install dependencies:")
        print("   pip install -r backend/requirements.txt")
        print("")
        print("3. Run unit tests:")
        print("   pytest backend/tests/unit/ -v")
        print("")
        print("4. Run integration tests:")
        print("   pytest backend/tests/integration/ -v")
        print("")
        print("5. Run full smoke test (with server):")
        print("   python backend/smoke_test.py")
        return 0

    except Exception as e:
        print(f"\n❌ SMOKE TEST FAILED: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
