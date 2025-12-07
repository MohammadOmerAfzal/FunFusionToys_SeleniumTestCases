import subprocess
import sys
import os

def run_test(script_name):
    print(f"\n==============================")
    print(f" Running {script_name}")
    print(f"==============================\n")

    result = subprocess.run(
        [sys.executable, script_name],
        cwd=".",  # current folder = /app/test
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception(f"{script_name} FAILED ❌")

    print(f"{script_name} PASSED ✅\n")


def main():

    print("\n====================================")
    print("   Starting Full Selenium Test Suite")
    print("====================================\n")

    # List of all Python Selenium test files
    test_scripts = [
        "test_register.py",
        "test_login.py",
        "productsPage.py",
        "test_product_details.py",
        "add_to_cart.py",
        "cart-actions.py",
        "cart_decrement.py",
        "test_cart_quantity.py",
        "checkout.py",
        "unauthorized_user_checkout.py",
    ]

    # Validation: make sure script exists before running
    missing = [t for t in test_scripts if not os.path.exists(t)]
    if missing:
        print("ERROR: Missing test files:", missing)
        sys.exit(1)

    # Run each test
    for script in test_scripts:
        run_test(script)

    print("\n====================================")
    print(" ALL TESTS PASSED SUCCESSFULLY 🎉🎉")
    print("====================================\n")


if __name__ == "__main__":
    main()

