import random

# Функция для вычисления количества проверочных битов (r)
# Формула: 2^r >= m + r + 1, где m — длина исходного сообщения
def calculate_redundant_bits(m):
    r = 1  # Начинаем с 1 проверочного бита
    while (2**r) < (m + r + 1):  # Проверяем, достаточно ли 2^r
        r += 1
    print(f"[calculate_redundant_bits] Длина данных: {m}, Требуется проверочных битов: {r} (2^{r} = {2**r} >= {m + r + 1})")
    return r

# Функция для вставки проверочных битов на позиции 1, 2, 4, 8, ...
# Вход: data — исходное сообщение (например, "1011"), r — число проверочных битов
# Выход: строка с данными и нулями на местах проверочных битов
def pos_redundant_bits(data, r):
    m = len(data)  # Длина исходного сообщения
    res = []
    j = 0  # Индекс для битов данных
    k = 0  # Индекс для позиций проверочных битов (2^k)
    print(f"[pos_redundant_bits] Вставка проверочных битов в сообщение: {data}")
    for i in range(1, m + r + 1):  # Проходим по всем позициям (1, 2, ..., m+r)
        if i == 2**k:  # Если позиция — степень двойки (1, 2, 4, ...)
            res.append('0')  # Вставляем 0 (позже вычислим значение)
            print(f"  Позиция {i} (2^{k}): Вставлен проверочный бит '0'")
            k += 1
        else:
            res.append(data[j])  # Вставляем бит из исходного сообщения
            print(f"  Позиция {i}: Вставлен бит данных '{data[j]}'")
            j += 1
    result = ''.join(res)
    print(f"[pos_redundant_bits] Результат: {result}")
    return result

# Функция для вычисления значений проверочных битов
# Вход: arr — сообщение с нулями на местах проверочных битов, r — число проверочных битов
# Каждый проверочный бит P_i (на позиции 2^i) проверяет позиции, где в двоичной записи номера позиции стоит 1 в i-м бите
# Значение P_i = XOR всех проверяемых битов
def calc_parity_bits(arr, r):
    n = len(arr)
    result = list(arr)
    print(f"[calc_parity_bits] Вычисление проверочных битов для: {arr}")
    for i in range(r):
        pos = 2**i  # Позиция проверочного бита (1, 2, 4, ...)
        val = 0  # Значение проверочного бита
        positions = []  # Список проверяемых позиций
        print(f"  Проверочный бит P{i+1} (позиция {pos}):")
        for j in range(1, n + 1):
            if j & pos:  # Проверяем, есть ли 1 в i-м бите номера позиции j
                val ^= int(arr[j - 1])  # XOR с битом на позиции j
                positions.append((j, arr[j - 1]))
        print(f"    Проверяемые позиции: {positions}")
        print(f"    XOR: {val}")
        result[pos - 1] = str(val)  # Устанавливаем значение проверочного бита
        print(f"    Установлен P{i+1} = {val} на позиции {pos}")
    final_result = ''.join(result)
    print(f"[calc_parity_bits] Закодированное сообщение: {final_result}")
    return final_result

# Функция для кодирования сообщения кодом Хэмминга
# Вход: data — исходное сообщение
# Выход: закодированное сообщение и число проверочных битов
def encode_hamming(data):
    m = len(data)
    print(f"[encode_hamming] Кодирование сообщения: {data}")
    r = calculate_redundant_bits(m)  # Вычисляем количество проверочных битов
    arr = pos_redundant_bits(data, r)  # Вставляем проверочные биты
    encoded = calc_parity_bits(arr, r)  # Вычисляем их значения
    print(f"[encode_hamming] Итог: Закодированное сообщение: {encoded}, Проверочных битов: {r}")
    return encoded, r

# Функция для внесения случайной ошибки
# Переворачивает один случайный бит (0 → 1 или 1 → 0)
def introduce_error(code):
    pos = random.randint(0, len(code) - 1)  # Выбираем случайную позицию
    code_list = list(code)
    old_bit = code_list[pos]
    code_list[pos] = '1' if code_list[pos] == '0' else '0'  # Переворачиваем бит
    result = ''.join(code_list)
    print(f"[introduce_error] Внесена ошибка: Позиция {pos + 1}, Бит '{old_bit}' изменен на '{code_list[pos]}'")
    print(f"[introduce_error] Сообщение с ошибкой: {result}")
    return result, pos + 1

# Функция для обнаружения ошибки
# Вход: code — сообщение с возможной ошибкой, r — число проверочных битов
# Вычисляет синдром, который указывает позицию ошибки (или 0, если ошибок нет)
def detect_error(code, r):
    n = len(code)
    syndrome = 0
    print(f"[detect_error] Вычисление синдрома для: {code}")
    for i in range(r):
        pos = 2**i
        val = 0
        positions = []
        print(f"  Проверочный бит P{i+1} (позиция {pos}):")
        for j in range(1, n + 1):
            if j & pos:  # Проверяем позиции, где i-й бит номера равен 1
                val ^= int(code[j - 1])
                positions.append((j, code[j - 1]))
        print(f"    Проверяемые позиции: {positions}")
        print(f"    XOR: {val}")
        syndrome += val * pos  # Вклад в синдром
        print(f"    Вклад в синдром: {val} * {pos} = {val * pos}")
    print(f"[detect_error] Синдром: {syndrome}")
    return syndrome

# Функция для исправления ошибки
# Если синдром ≠ 0, переворачивает бит в позиции, указанной синдромом
def correct_error(code, syndrome):
    print(f"[correct_error] Исправление ошибки, синдром: {syndrome}")
    if syndrome == 0:
        print(f"[correct_error] Ошибок нет")
        return code, "Ошибок нет"
    code_list = list(code)
    old_bit = code_list[syndrome - 1]
    code_list[syndrome - 1] = '1' if code_list[syndrome - 1] == '0' else '0'
    result = ''.join(code_list)
    print(f"[correct_error] Исправлена ошибка в позиции {syndrome}: Бит '{old_bit}' изменен на '{code_list[syndrome - 1]}'")
    print(f"[correct_error] Исправленное сообщение: {result}")
    return result, f"Ошибка в позиции {syndrome}"

# Функция для декодирования
# Удаляет проверочные биты, возвращает исходное сообщение
def decode_hamming(code, r):
    print(f"[decode_hamming] Декодирование сообщения: {code}")
    decoded = []
    parity_positions = [2**j for j in range(r)]  # Позиции проверочных битов
    for i in range(1, len(code) + 1):
        if i not in parity_positions:
            decoded.append(code[i - 1])
            print(f"  Позиция {i}: Извлечен бит данных '{code[i - 1]}'")
        else:
            print(f"  Позиция {i}: Пропущен проверочный бит")
    result = ''.join(decoded)
    print(f"[decode_hamming] Декодированное сообщение: {result}")
    return result

# Основная функция
def main():
    # Получаем входное сообщение
    data = input("Введите бинарное сообщение (например, 1011): ")
    if not all(c in '01' for c in data):
        print("Ошибка: Введите только 0 и 1")
        return

    # Кодирование
    print("\n=== Кодирование ===")
    encoded, r = encode_hamming(data)
    print(f"Исходное сообщение: {data}")
    print(f"Закодированное сообщение: {encoded}")
    print(f"Количество проверочных битов: {r}")

    # Ввод ошибки
    choice = input("\nВнести случайную ошибку? (y/n): ").lower()
    if choice == 'y':
        corrupted, error_pos = introduce_error(encoded)
        print(f"\n=== Внесение ошибки ===")
        print(f"Сообщение с ошибкой: {corrupted}")
        print(f"Ошибка внесена в позицию: {error_pos}")
    else:
        corrupted = encoded
        print("\n=== Внесение ошибки ===")
        print("Ошибки не вносились")
        print(f"Сообщение: {corrupted}")

    # Обнаружение и исправление ошибки
    print("\n=== Обнаружение и исправление ошибки ===")
    syndrome = detect_error(corrupted, r)
    corrected, message = correct_error(corrupted, syndrome)
    print(f"Синдром: {syndrome}")
    print(f"Результат: {message}")
    print(f"Исправленное сообщение: {corrected}")

    # Декодирование
    print("\n=== Декодирование ===")
    decoded = decode_hamming(corrected, r)
    print(f"Декодированное сообщение: {decoded}")
    if decoded == data:
        print("Декодирование успешно: исходное сообщение восстановлено!")
    else:
        print("Ошибка: декодированное сообщение отличается от исходного.")

if __name__ == "__main__":
    main()