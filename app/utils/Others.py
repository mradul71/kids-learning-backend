import random, string

def generate_password() -> str:
    print("password22")
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    password = random.choices(characters , k = 10)
    random.shuffle(password)
    print(password)
    return "".join(password)