import re
from typing import Annotated, get_type_hints

# Your original setup
Email = Annotated[str, "This has to be valid email format"]

def register_user(email: Email):
    validate_email(email)
    print(f"Successfully registered: {email}")

def validate_email(email_value: str):
    """Checks if the email matches a standard pattern."""
    # 1. Access the metadata via get_type_hints
    # We look at 'register_user' to see what rules 'email' should follow
    hints = get_type_hints(register_user, include_extras=True)
    metadata = hints['email'].__metadata__[0]
    
    # 2. Perform the actual test (Simple Regex for email)
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    if not re.match(email_pattern, email_value):
        # We use the metadata string in our error message!
        raise ValueError(f"Validation Failed: {metadata}. Received: '{email_value}'")
    
    return True

# --- TESTING IT ---

print("--- Test 1: Valid Email ---")
register_user("bob@example.com") # Works!

print("\n--- Test 2: Invalid Email ---")
try:
    register_user("bad-email-no-at-symbol")
except ValueError as e:
    print(e)