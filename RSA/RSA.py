import random
import math

def is_prime(n):
    """Проверяет, является ли число простым."""
    # Если число меньше 2, оно не простое
    if n < 2:
        print(f"[is_prime] Число {n} меньше 2, не простое")
        return False
    # Проверяем делители от 2 до sqrt(n)
    print(f"[is_prime] Проверка числа {n} на простоту")
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            print(f"[is_prime] Число {n} делится на {i}, не простое")
            return False
    print(f"[is_prime] Число {n} простое")
    return True

def generate_prime(min_value, max_value):
    """Генерирует случайное простое число в заданном диапазоне."""
    # Генерируем случайное число в диапазоне [min_value, max_value]
    prime = random.randint(min_value, max_value)
    print(f"[generate_prime] Сгенерировано число: {prime}")
    # Проверяем, простое ли оно; если нет, генерируем новое
    while not is_prime(prime):
        print(f"[generate_prime] Число {prime} не простое, генерация нового")
        prime = random.randint(min_value, max_value)
        print(f"[generate_prime] Сгенерировано новое число: {prime}")
    print(f"[generate_prime] Найдено простое число: {prime}")
    return prime

def mod_inverse(e, phi):
    """Вычисляет модульный мультипликативный обратный элемент для e по модулю phi."""
    print(f"[mod_inverse] Поиск обратного элемента для e={e}, phi={phi}")
    # Перебираем числа d, пока не найдем такое, что (d * e) % phi == 1
    for d in range(3, phi):
        if (d * e) % phi == 1:
            print(f"[mod_inverse] Найден обратный элемент: d={d} (({d} * {e}) % {phi} = 1)")
            return d
    # Если обратный элемент не найден, вызываем ошибку
    print(f"[mod_inverse] Обратный элемент для e={e}, phi={phi} не существует")
    raise ValueError("Модульный обратный элемент не существует")

def generate_keypair(min_value=100, max_value=1000):
    """Генерирует пару открытого и закрытого ключей для RSA."""
    print("[generate_keypair] Начало генерации ключей")
    # Генерируем два простых числа p и q
    print("[generate_keypair] Генерация первого простого числа p")
    p = generate_prime(min_value, max_value)
    print("[generate_keypair] Генерация второго простого числа q")
    q = generate_prime(min_value, max_value)
    print(f"[generate_keypair] p={p}, q={q}")

    # Вычисляем n = p * q (модуль для ключей)
    n = p * q
    print(f"[generate_keypair] Вычислено n = p * q = {p} * {q} = {n}")

    # Вычисляем phi = (p-1)(q-1) (функция Эйлера)
    phi = (p - 1) * (q - 1)
    print(f"[generate_keypair] Вычислено phi = (p-1)(q-1) = ({p}-1)({q}-1) = {phi}")

    # Выбираем e: 1 < e < phi, взаимно простое с phi (открытая экспонента)
    e = random.randint(3, phi - 1)
    print(f"[generate_keypair] Выбрано случайное e={e}")
    while math.gcd(e, phi) != 1:
        print(f"[generate_keypair] e={e} не взаимно простое с phi={phi} (НОД={math.gcd(e, phi)}), выбор нового e")
        e = random.randint(3, phi - 1)
        print(f"[generate_keypair] Новое e={e}")
    print(f"[generate_keypair] Окончательное e={e} (НОД(e, phi) = {math.gcd(e, phi)})")

    # Вычисляем d, модульный обратный элемент для e (закрытая экспонента)
    print("[generate_keypair] Вычисление d (модульного обратного для e)")
    d = mod_inverse(e, phi)
    print(f"[generate_keypair] d={d}")

    # Возвращаем открытый ключ (e, n) и закрытый ключ (d, n)
    print(f"[generate_keypair] Открытый ключ: (e={e}, n={n}), Закрытый ключ: (d={d}, n={n})")
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """Шифрует текст с использованием открытого ключа."""
    e, n = public_key
    print(f"[encrypt] Шифрование сообщения: '{plaintext}' с открытым ключом (e={e}, n={n})")
    # Преобразуем каждый символ в число (ASCII) и шифруем: c = m^e mod n
    cipher = []
    for i, char in enumerate(plaintext):
        m = ord(char)
        c = pow(m, e, n)
        print(f"[encrypt] Символ '{char}' (ASCII={m}): {m}^{e} mod {n} = {c}")
        cipher.append(c)
    print(f"[encrypt] Зашифрованное сообщение: {cipher}")
    return cipher

def decrypt(private_key, ciphertext):
    """Расшифровывает текст с использованием закрытого ключа."""
    d, n = private_key
    print(f"[decrypt] Расшифровка сообщения: {ciphertext} с закрытым ключом (d={d}, n={n})")
    # Расшифровываем каждое число обратно в символ: m = c^d mod n
    plain = []
    for i, c in enumerate(ciphertext):
        m = pow(c, d, n)
        char = chr(m)
        print(f"[decrypt] Число {c}: {c}^{d} mod {n} = {m} (символ '{char}')")
        plain.append(char)
    result = ''.join(plain)
    print(f"[decrypt] Расшифрованное сообщение: '{result}'")
    return result

def main():
    """Основная функция для демонстрации работы RSA."""
    print("[main] Запуск программы RSA")
    # Генерируем ключи
    print("[main] Генерация ключей")
    public_key, private_key = generate_keypair()
    print("[main] Открытый ключ:", public_key)
    print("[main] Закрытый ключ:", private_key)

    # Получаем сообщение для шифрования
    message = input("[main] Введите сообщение для шифрования: ")
    print(f"[main] Введенное сообщение: '{message}'")

    # Шифруем сообщение
    print("[main] Шифрование сообщения")
    encrypted_msg = encrypt(public_key, message)
    print("[main] Зашифрованное сообщение:", encrypted_msg)

    # Расшифровываем сообщение
    print("[main] Расшифровка сообщения")
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print("[main] Расшифрованное сообщение:", decrypted_msg)

if __name__ == '__main__':
    main()