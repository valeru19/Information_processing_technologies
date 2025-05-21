import math


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида: возвращает (gcd, x, y), где gcd = ax + by."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    """Находит мультипликативный обратный элемент a^(-1) mod m."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return x % m


def gcd(a, b):
    """Вычисляет НОД двух чисел."""
    while b:
        a, b = b, a % b
    return a


def is_perfect_power(n):
    """Проверяет, является ли n степенью (a^b, b > 1)."""
    for b in range(2, int(math.log2(n)) + 1):  # b — показатель степени, int(math.log2(n)) + 1 — верхняя граница для b
        a = round(n ** (
                    1.0 / b))  # round — округляет число до ближайшего целого, используется для нахождения a как корня b-й степени из n
        if a ** b == n:
            return True
    return False


def get_largest_prime_factor(n):
    """Находит наибольший простой делитель n."""
    i = 2  # i — текущий делитель, начинаем с 2 (первого простого числа)
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            if n == 1:
                return i
        i += 1
    return n if n > 1 else i - 1


def poly_mod(poly, r, n):
    """Приводит полином по модулю x^r - 1 и N."""
    result = [0] * r  # result — список коэффициентов результирующего полинома, инициализируется нулями длиной r
    for i in range(len(poly)):  # i — индекс коэффициента исходного полинома poly
        idx = i % r  # idx — индекс в результирующем полиноме после приведения по модулю r (x^r ≡ 1)
        result[idx] = (result[idx] + poly[i]) % n  # poly[i] — коэффициент при x^i, % n — остаток по модулю N
    return result


def poly_multiply(p1, p2, r, n):
    """Умножает полиномы p1 и p2 по модулю x^r - 1 и N."""
    result = [0] * (len(p1) + len(
        p2) - 1)  # result — список для хранения результата умножения, длина равна сумме степеней p1 и p2 минус 1
    for i in range(len(p1)):  # i — индекс коэффициента первого полинома p1
        for j in range(len(p2)):  # j — индекс коэффициента второго полинома p2
            result[i + j] = (result[i + j] + p1[i] * p2[
                j]) % n  # Умножение коэффициентов и суммирование с учетом модуля n
    return poly_mod(result, r, n)


def poly_power(poly, exponent, r, n):
    """Возводит полином в степень exponent по модулю x^r - 1 и N."""
    if exponent == 0:
        return [1] + [0] * (r - 1)  # Возвращает полином 1 (единичный полином) при нулевой степени
    if exponent == 1:
        return poly_mod(poly, r, n)
    result = [1] + [0] * (r - 1)  # result — начальный полином (1), длина r
    base = poly_mod(poly, r, n)  # base — копия полинома poly, приведенная по модулю
    while exponent > 0:
        if exponent % 2 == 1:  # % 2 — остаток от деления на 2, проверяет нечетность
            result = poly_multiply(result, base, r, n)
        base = poly_multiply(base, base, r, n)
        exponent //= 2  # //= — целочисленное деление с присваиванием для бинарного возведения
    return result


def poly_subtract(p1, p2, n):
    """Вычитает p2 из p1 по модулю N."""
    length = max(len(p1), len(p2))  # length — максимальная длина полиномов для выравнивания
    p1 = p1 + [0] * (length - len(p1))  # Дополняем p1 нулями до length
    p2 = p2 + [0] * (length - len(p2))  # Дополняем p2 нулями до length
    return [(p1[i] - p2[i]) % n for i in
            range(length)]  # Вычитание с учетом модуля n, list comprehension — компактный цикл


def is_poly_zero(poly, n):
    """Проверяет, нулевой ли полином по модулю N."""
    return all(coef % n == 0 for coef in
               poly)  # all — возвращает True, если все элементы удовлетворяют условию (coef % n == 0)


def check_congruence(a, N, r):
    """Проверяет (x - a)^N ≡ x^N - a (mod x^r - 1, N)."""
    poly_x_minus_a = [(-a) % N, 1]  # poly_x_minus_a — полином (x - a), где первый коэффициент -a mod N, второй 1
    left = poly_power(poly_x_minus_a, N, r, N)  # left — (x - a)^N по модулю
    right = [0] * r  # right — полином x^N - a, инициализируется нулями длиной r
    right[N % r] = 1  # Устанавливаем 1 на позиции N % r для x^N
    right[0] = (-a) % N  # Устанавливаем -a mod N как свободный член
    right = poly_mod(right, r, N)
    diff = poly_subtract(left, right, N)  # diff — разность полиномов
    return is_poly_zero(diff, N)


def is_prime(n):
    """Реализует Алгоритм 5.4 для проверки простоты числа n."""
    print(f"\n=== Проверка N = {n} ===")

    # Шаг 1: Проверяем, является ли N степенью (например, 9 = 3^2)
    if is_perfect_power(n):
        print(f"Шаг 1: N = {n} — это степень (a^b, b > 1). Вывод: составное.")
        return False
    print("Шаг 1: N не является степенью. Переходим к следующему шагу.")

    # Шаг 2: Инициализируем r = 2
    r = 2  # r — параметр для проверки, начинаем с 2
    print(f"Шаг 2: Устанавливаем r = {r}.")

    # Шаги 3–8: Цикл по r, пока r < N
    while r < n:
        print(f"Шаг 3: Проверяем r = {r}.")

        # Шаг 4: Проверяем, делит ли r число N
        d = gcd(r, n)  # d — НОД(r, n)
        if d > 1:
            print(f"Шаг 4: НОД({r}, {n}) = {d} > 1. Вывод: N составное.")
            return False

        # Шаг 5: Проверяем, простое ли r
        if all(r % i != 0 for i in
               range(2, int(math.sqrt(r)) + 1)):  # all — проверяет, что r не делится ни на одно число до его корня
            print(f"Шаг 5: r = {r} простое.")
            # Шаг 6: Находим q — наибольший простой делитель (r-1)
            q = get_largest_prime_factor(r - 1)  # q — наибольший простой делитель r-1
            print(f"Шаг 6: Наибольший простой делитель числа {r - 1} равен q = {q}.")

            # Шаг 7: Проверяем условия для r
            log_n = math.log2(n)  # log_n — логарифм по основанию 2 от n
            if q * r >= 4 * log_n ** 2:
                inv = mod_inverse(r - 1, r)  # inv — обратный элемент (r-1)^(-1) mod r
                if inv is None or pow(n, inv, r) != 1:
                    print(f"Шаг 7: r = {r} подходит для проверки. Переходим к шагу 9.")
                    break
            print(f"Шаг 7: r = {r} не подходит. Увеличиваем r.")

        r += 1
        if r == n:
            print(f"Шаг 8: r достиг N ({r} = {n}). Вывод: N простое.")
            return True

    # Шаг 9: Проверяем сравнение (x - a)^N ≡ x^N - a для нескольких a
    print(f"Шаг 9: Используем r = {r} для проверки сравнений.")
    log_n_ceil = math.ceil(2 * log_n ** 2)  # log_n_ceil — верхняя граница для a, округление вверх
    threshold = r * math.ceil(2 * log_n ** 2)  # threshold — порог для выбора диапазона a
    if n <= threshold:
        print(f"Шаг 9: Проверяем числа a до {min(r ** (n - 1), 100)}.")
        for a in range(1, min(r ** (n - 1), 100)):  # a — переменная для проверки сравнения
            if gcd(a, n) > 1:
                print(f"Шаг 9: НОД({a}, {n}) = {gcd(a, n)} > 1. Вывод: N составное.")
                return False
    else:
        print(f"Шаг 9: Проверяем числа a от 1 до {log_n_ceil}.")
        for a in range(1, log_n_ceil + 1):
            if gcd(a, n) > 1:
                print(f"Шаг 9: НОД({a}, {n}) = {gcd(a, n)} > 1. Вывод: N составное.")
                return False
            print(f"Шаг 9: Проверяем a = {a}: сравнение (x - {a})^N ≡ x^N - {a}.")
            if not check_congruence(a, n, r):
                print(f"Шаг 9: Сравнение для a = {a} не выполнено. Вывод: N составное.")
                return False

    # Шаг 10: Если все проверки пройдены, N простое
    print("Шаг 10: Все сравнения выполнены. Вывод: N простое.")
    return True


# Тестовые примеры
for n in [7, 9, 15, 10, 21, 11]:
    is_prime(n)