import secrets
import string

def generate_random_code(length: int, use_letters: bool = True) -> str:
    if use_letters:
        characters = string.ascii_uppercase + string.digits
    else:
        characters = string.digits
    
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code