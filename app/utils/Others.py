import random, string

def generate_password() -> str:
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    password = random.choices(characters , k = 10)
    random.shuffle(password)
    return "".join(password)

def generate_random_id(length: int=25) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))