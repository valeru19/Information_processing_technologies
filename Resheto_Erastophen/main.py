def sieve_of_eratosthenes_with_steps(n):
    """
    Функция реализует алгоритм "Решето Эратосфена" для поиска всех простых чисел до n.
    Содержит подробные комментарии и пошаговый вывод для лучшего понимания алгоритма.
    """

    # Проверка на случай, если пользователь ввел число меньше 2
    if n < 2:
        print("Нет простых чисел меньше 2.")
        return []

    # Создаем "решето" - список из булевых значений, изначально все True
    # Индексы списка соответствуют числам от 0 до n
    # sieve[i] = True означает, что число i считается потенциально простым
    sieve = [True] * (n + 1)

    # 0 и 1 не являются простыми числами
    sieve[0] = sieve[1] = False

    print("\nИнициализация решета:")
    print(f"Создан список длиной {n + 1}, где каждый элемент = True")
    print("0 и 1 помечены как False (не простые)")
    print("Текущее состояние решета:")
    print([i if sieve[i] else "X" for i in range(n + 1)])  # X - вычеркнутые числа

    # Основной цикл алгоритма
    # Перебираем числа от 2 до квадратного корня из n
    # (так как составные числа > sqrt(n) уже будут вычеркнуты их делителями)
    for current in range(2, int(n ** 0.5) + 1):
        if sieve[current]:  # Если current еще не вычеркнуто, значит оно простое
            print(f"\nНайдено простое число: {current}")
            print(f"Вычеркиваем все кратные {current}, начиная с {current}^2 = {current * current}")

            # Вычеркиваем все кратные current, начиная с current^2
            # (все меньшие кратные уже были вычеркнуты на предыдущих шагах)
            for multiple in range(current * current, n + 1, current):
                if sieve[multiple]:
                    sieve[multiple] = False
                    print(f"  Вычеркиваем {multiple} ( = {current} * {multiple // current})")

            # Выводим текущее состояние решета после вычеркивания
            print("\nТекущее состояние решета:")
            print([i if sieve[i] else "X" for i in range(n + 1)])

            # Пауза для удобства просмотра (раскомментируйте, если нужно)
            # input("Нажмите Enter для продолжения...")

    # Собираем все числа, оставшиеся невычеркнутыми (простые числа)
    primes = [i for i, is_prime in enumerate(sieve) if is_prime]

    print("\nПроцесс завершен. Все составные числа вычеркнуты.")
    return primes


# Основная часть программы
print("Алгоритм: Решето Эратосфена")
print("Находит все простые числа до заданного N")
print("=" * 50)

try:
    # Запрос ввода от пользователя
    n = int(input("Введите число N (N ≥ 2): "))

    # Проверка на корректность ввода
    if n < 2:
        print("Ошибка: N должно быть ≥ 2")
    else:
        # Выполняем алгоритм и получаем результат
        primes = sieve_of_eratosthenes_with_steps(n)

        # Выводим итоговый результат
        print("\n" + "=" * 50)
        print(f"Все простые числа до {n}:")
        print(primes)
        print(f"Найдено {len(primes)} простых чисел")

except ValueError:
    print("Ошибка: введите целое число")