#C:\Users\waler\Downloads\Telegram Desktop\_Donald_Knut_Iskusstvo_programmirovaniya,_tom_3BookFi стр. 445
import math

# Функция для вычисления DELTA[j]
def compute_delta(N, j):
    if 1 <= j <= math.ceil(math.log2(N)) + 2:
        return (N + 2**(j-1)) // (2**j)
    return 0

# Функция для получения ключа K_i
def get_key_at_index(i, N):
    if i == 0:
        return float('-inf')
    if 1 <= i <= N:
        return i
    return float('inf')

# Программа C: одновременный бинарный поиск с подробным выводом
def program_C(N, K):
    # C1: Инициализация
    i = (N + 1) // 2
    j = 2
    print(f"C1: Инициализация: i = {i}, j = {j}")

    # Для отладки: выводим DELTA
    delta = {}
    for j_val in range(1, math.ceil(math.log2(N)) + 3):
        delta[j_val] = compute_delta(N, j_val)
    print(f"DELTA: {delta}")

    # Инициализация диапазона
    left = 0
    right = 30
    print(f"Начальный диапазон поиска: [{left}, {right}]")

    comparisons = 0

    while True:
        K_i = get_key_at_index(i, N)
        comparisons += 1
        delta_j = compute_delta(N, j)

        # Вывод текущего состояния
        print(f"\nШаг {comparisons}:")
        print(f"  Текущий диапазон: [{left}, {right}]")
        print(f"  i = {i}, j = {j}, K = {K}, K_i = {K_i}, DELTA[{j}] = {delta_j}")

        # C2: Сравнение K с K_i
        if K == K_i and 1 <= i <= N:
            print(f"  C2: Успех, K = K_i = {K}, i = {i}")
            print(f"  Итоговый диапазон: [{i}, {i}] (найдено точное значение)")
            return i, comparisons
        elif K < K_i:
            print(f"  C2: K < K_i, переходим к C3")
            # C3: Уменьшение i
            if delta_j == 0:
                print(f"  C3: DELTA[{j}] = 0, неудачное завершение")
                print(f"  Итоговый диапазон: [{left}, {right}] (не удалось найти точное значение)")
                return None, comparisons
            i = i - delta_j
            j = j + 1
            # Обновляем верхнюю границу диапазона
            right = min(right, K_i - 1)
            print(f"  C3: Уменьшаем i: новый i = {i}, новый j = {j}, DELTA[{j-1}] = {delta_j}")
            print(f"  Новый диапазон: [{left}, {right}]")
        else:  # K > K_i
            print(f"  C2: K > K_i, переходим к C4")
            # C4: Увеличение i
            if delta_j == 0:
                print(f"  C4: DELTA[{j}] = 0, неудачное завершение")
                print(f"  Итоговый диапазон: [{left}, {right}] (не удалось найти точное значение)")
                return None, comparisons
            i = i + delta_j
            j = j + 1
            # Обновляем нижнюю границу диапазона
            left = max(left, K_i + 1)
            print(f"  C4: Увеличиваем i: новый i = {i}, новый j = {j}, DELTA[{j-1}] = {delta_j}")
            print(f"  Новый диапазон: [{left}, {right}]")

# Программа B: запуск программы C
def program_B(N):
    print(f"Программа B: Запускаем программу C для N = {N}")
    # Устанавливаем K = N, так как ищем N
    K = N
    result, comparisons = program_C(N, K)
    if result is not None:
        print(f"\nПрограмма B: Найденное значение N = {result}, количество сравнений = {comparisons}")
    else:
        print(f"\nПрограмма B: Не удалось найти N, количество сравнений = {comparisons}")
    return result, comparisons

# Тестирование
if __name__ == "__main__":
    N = 22
    print(f"Тестирование для N = {N}")
    found_N, comparisons = program_B(N)