from math import gcd
from itertools import product


# Функция для вычисления символа Лежандра (a/p)
# Символ Лежандра определяет, является ли a квадратным вычетом по модулю простого p
# Формула: (a/p) = a^((p-1)/2) mod p
# Возвращает:
#   0, если a ≡ 0 (mod p)
#   1, если a — квадратный вычет (существует x, такое что x^2 ≡ a (mod p))
#   -1, если a — неквадратный вычет (нет такого x)
def legendre_symbol(a, p):
    if a % p == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return result if result <= 1 else -1  # Нормализуем: p-1 ≡ -1 (mod p)


# Функция для нахождения квадратных корней числа a по модулю простого p
# Решает уравнение x^2 ≡ a (mod p)
# Если a — не квадратный вычет ((a/p) ≠ 1), возвращает пустой список
# Для p > 2 перебирает r, пока не найдет r^2 ≡ a (mod p)
# Возвращает оба корня: r и -r (mod p)
def sqrt_mod(a, p):
    if legendre_symbol(a, p) != 1:  # Проверяем, является ли a квадратным вычетом
        return []
    if p == 2:  # Особый случай для p = 2
        return [a % 2]
    for r in range(1, p):
        if (r * r) % p == a:
            return [r, (-r) % p]  # Возвращаем оба корня: r и -r
    return []


# Функция для решения системы сравнений x ≡ b_i (mod q_i) с помощью Китайской теоремы об остатках
# Формула: x = Σ (b_i * N_i * inv_i) mod N, где
#   N = q_1 * q_2 * ... * q_n — произведение модулей
#   N_i = N / q_i
#   inv_i — обратный элемент N_i по модулю q_i (N_i * inv_i ≡ 1 (mod q_i))
# Модули q_i должны быть попарно взаимно простыми (gcd(q_i, q_j) = 1 для i ≠ j)
def chinese_remainder_theorem(moduli, remainders):
    if len(moduli) != len(remainders):
        return None
    N = 1  # Вычисляем N = q_1 * q_2 * ... * q_n
    for m in moduli:
        N *= m
    # Проверяем, что модули попарно взаимно простые
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                return None
    result = 0
    for i in range(len(moduli)):
        Ni = N // moduli[i]
        inv = pow(Ni, -1, moduli[i])  # Обратный элемент N_i по модулю q_i
        result += remainders[i] * Ni * inv
    return result % N


# Основная функция для реализации теоремы 7.1
# Теорема 7.1: Если v — квадратный вычет по каждому q_i ((v/q_i) = 1),
# а u — неквадратный вычет ((u/q_i) = -1), то существует 2^n решений
# уравнения x^2 ≡ v (mod q), где q = q_1 * q_2 * ... * q_n,
# и нет решений x^2 ≡ u (mod q_i) для любого q_i
def theorem_7_1(q_list, v, u):
    print(f"\n=== Проверка теоремы 7.1 для v = {v}, u = {u}, q_i = {q_list} ===")

    # Шаг 1: Проверяем, является ли v квадратным вычетом, а u — невычетом
    print("\nШаг 1: Проверка символов Лежандра")
    print("Символ Лежандра (a/p) определяется как (a/p) = a^((p-1)/2) mod p")
    print("Ожидаем: (v/q_i) = 1 (v — квадратный вычет), (u/q_i) = -1 (u — невычет)")
    for q_i in q_list:
        v_symbol = legendre_symbol(v, q_i)
        u_symbol = legendre_symbol(u, q_i)
        print(f"\nПо модулю q_i = {q_i}:")
        print(f"  (v/q_i) = ({v}/{q_i}) = {v}^(({q_i}-1)/2) mod {q_i} = {v_symbol}")
        print(f"  (u/q_i) = ({u}/{q_i}) = {u}^(({q_i}-1)/2) mod {q_i} = {u_symbol}")
        if v_symbol != 1:
            print(f"Ошибка: v = {v} не является квадратным вычетом по модулю {q_i} ((v/q_i) ≠ 1).")
            print("Теорема 7.1 не применима.")
            return
        if u_symbol != -1:
            print(f"Ошибка: u = {u} не является неквадратным вычетом по модулю {q_i} ((u/q_i) ≠ -1).")
            print("Теорема 7.1 не применима.")
            return

    # Шаг 2: Находим квадратные корни v по каждому q_i
    print("\nШаг 2: Нахождение квадратных корней v по каждому q_i")
    print("Решаем уравнение x^2 ≡ v (mod q_i) для каждого q_i")
    roots_per_q = []
    for q_i in q_list:
        roots = sqrt_mod(v, q_i)
        print(f"\nПо модулю q_i = {q_i}:")
        print(f"  Корни уравнения x^2 ≡ {v} (mod {q_i}): {roots}")
        if not roots:
            print(f"Ошибка: Не удалось найти корни для v = {v} по модулю {q_i}.")
            return
        roots_per_q.append(roots)

    # Шаг 3: Находим все комбинации корней по Китайской теореме об остатках
    print("\nШаг 3: Объединение корней с помощью Китайской теоремы об остатках")
    q = 1
    for q_i in q_list:
        q *= q_i
    print(f"Модуль q = Π q_i = {q}")
    print(f"Ожидаемое количество корней: 2^{len(q_list)} = {2 ** len(q_list)}")
    print("Для каждого q_i есть 2 корня, поэтому всего 2^n комбинаций")

    all_solutions = []
    for root_combination in product(*roots_per_q):
        print(f"\nКомбинация корней: {root_combination}")
        print(f"Решаем систему сравнений:")
        for i, (q_i, r_i) in enumerate(zip(q_list, root_combination)):
            print(f"  x ≡ {r_i} (mod {q_i})")
        x0 = chinese_remainder_theorem(q_list, root_combination)
        if x0 is not None:
            print(f"Решение: x ≡ {x0} (mod {q})")
            all_solutions.append(x0)
        else:
            print("Ошибка: Не удалось найти решение для этой комбинации.")

    print(f"\nВсе квадратные корни v = {v} по модулю q = {q}: {sorted(all_solutions)}")
    print(f"Количество найденных корней: {len(all_solutions)} (ожидается {2 ** len(q_list)})")

    # Шаг 4: Проверяем, что u не имеет корней
    print("\nШаг 4: Проверка, что u не имеет квадратных корней")
    print("Проверяем, что уравнение x^2 ≡ u (mod q_i) не имеет решений")
    for q_i in q_list:
        u_roots = sqrt_mod(u, q_i)
        print(f"\nПо модулю q_i = {q_i}:")
        print(f"  Корни уравнения x^2 ≡ {u} (mod {q_i}): {u_roots}")
        if u_roots:
            print(f"Ошибка: u = {u} имеет корни {u_roots} по модулю {q_i}, хотя не должен.")
            return
    print(f"\nУспех: u = {u} не имеет квадратных корней по всем q_i, как ожидалось.")
    print(f"Теорема 7.1 успешно применена!")


# Пример использования
q_list = [3, 5, 7]  # Список простых чисел q_i
v = 1  # Число v (должно быть квадратным вычетом)
u = 17  # Число u (должно быть неквадратным вычетом)

theorem_7_1(q_list, v, u)