# 146 стр

from math import gcd

# Функция для вычисления символа Лежандра (a/p)
def legendre_symbol(a, p):
    if a % p == 0:
        return 0
    return pow(a, (p - 1) // 2, p)  # Символ Лежандра: 1 если вычет, -1 если невычет

# Функция для нахождения квадратных корней числа a по модулю простого p
def sqrt_mod(a, p):
    if legendre_symbol(a, p) != 1:  # Если a — не квадратный вычет
        return []
    if p == 2:
        return [a % 2]
    # Используем алгоритм Тонелли-Шенкса для простых p > 2
    # Находим корни r и -r такие, что r^2 ≡ a (mod p)
    for r in range(1, p):
        if (r * r) % p == a:
            return [r, (-r) % p]  # Возвращаем оба корня
    return []

# Функция для решения системы сравнений вида x ≡ b_i (mod q_i) с помощью Китайской теоремы об остатках
def chinese_remainder_theorem(moduli, remainders):
    # Проверяем, что длины совпадают
    if len(moduli) != len(remainders):
        return None
    # Вычисляем произведение всех модулей
    N = 1
    for m in moduli:
        N *= m
    # Проверяем, что модули попарно взаимно простые
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                return None  # Модули должны быть взаимно простыми
    # Решаем систему
    result = 0
    for i in range(len(moduli)):
        Ni = N // moduli[i]
        # Находим обратный элемент Ni по модулю moduli[i]
        inv = pow(Ni, -1, moduli[i])
        result += remainders[i] * Ni * inv
    return result % N

# Основная функция для реализации теоремы 7.1
def theorem_7_1(q_list, v, u):
    # Шаг 1: Проверяем, является ли v квадратным вычетом, а u — невычетом
    print(f"Проверяем v = {v} и u = {u} по модулю q_i:")
    for q_i in q_list:
        v_symbol = legendre_symbol(v, q_i)
        u_symbol = legendre_symbol(u, q_i)
        print(f"q_i = {q_i}: символ Лежандра (v/q_i) = {v_symbol}, (u/q_i) = {u_symbol}")
        if v_symbol != 1:
            print(f"v = {v} не является квадратным вычетом по модулю {q_i}. Теорема не применима.")
            return
        if u_symbol == 1:
            print(f"u = {u} является квадратным вычетом по модулю {q_i}, что противоречит условию.")
            return

    # Шаг 2: Находим квадратные корни v по каждому q_i
    roots_per_q = []
    for q_i in q_list:
        roots = sqrt_mod(v, q_i)
        print(f"Квадратные корни v = {v} по модулю {q_i}: {roots}")
        roots_per_q.append(roots)

    # Шаг 3: Находим все комбинации корней по Китайской теореме об остатках
    q = 1
    for q_i in q_list:
        q *= q_i
    print(f"\nМодуль q = {q}")
    print(f"Ожидаемое количество корней: 2^{len(q_list)} = {2**len(q_list)}")

    # Генерируем все возможные комбинации корней
    all_solutions = []
    from itertools import product
    for root_combination in product(*roots_per_q):
        x0 = chinese_remainder_theorem(q_list, root_combination)
        if x0 is not None:
            all_solutions.append(x0)

    print(f"Все квадратные корни v = {v} по модулю {q}: {sorted(all_solutions)}")

    # Шаг 4: Проверяем, что u не имеет корней
    for q_i in q_list:
        u_roots = sqrt_mod(u, q_i)
        if u_roots:
            print(f"Ошибка: u = {u} имеет корни {u_roots} по модулю {q_i}, хотя не должен.")
            return
    print(f"u = {u} не имеет квадратных корней, как и ожидалось.")

# Пример использования
q_list = [3, 5, 7]  # Список простых чисел q_i
v = 1  # Число v (должно быть квадратным вычетом)
u = 2  # Число u (должно быть квадратным невычетом)

theorem_7_1(q_list, v, u)