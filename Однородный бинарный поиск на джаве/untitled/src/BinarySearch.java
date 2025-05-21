public class BinarySearch {
    // Переменная для подсчёта количества сравнений
    static int comparisons = 0;

    // Метод, который имитирует запуск программы K раз
    // Если K <= N, возвращаем true (успех), иначе false (неудача)
    static boolean runProgram(int K, int N) {
        comparisons++; // Увеличиваем счётчик сравнений
        System.out.println("Пробуем K = " + K);
        if (K <= N) {
            System.out.println("Успех: K = " + K + " <= N");
            return true;
        } else {
            System.out.println("Неудача: K = " + K + " > N");
            return false;
        }
    }

    // Главный метод, который запускает программу
    public static void main(String[] args) {
        // Заданное N (для теста)
        int N = 10;
        System.out.println("Заданное N = " + N);

        // Определяем начальный диапазон
        // lg N — это логарифм по основанию 2
        double lgN = Math.log(N) / Math.log(2); // lg 10 ≈ 3.32
        int upperBound = (int) Math.ceil(lgN) + 2; // ⌈lg N⌉ + 2
        int left = 1; // Левая граница
        int right = 15; // Правая граница (берём 15 как в примере)
        System.out.println("Начальный диапазон: от " + left + " до " + right);

        // Сбрасываем счётчик сравнений
        comparisons = 0;

        // Бинарный поиск
        while (left < right) {
            // Находим середину диапазона
            int K = (left + right) / 2; // Целое деление
            System.out.println("Диапазон: от " + left + " до " + right);

            // Проверяем, работает ли программа при K запусках
            if (runProgram(K, N)) { // Успех
                left = K; // Сужаем диапазон: N >= K
            } else { // Неудача
                right = K; // Сужаем диапазон: N < K
            }

            // Если left и right сошлись, делаем последнее сравнение
            if (right - left == 1) {
                K = left;
                if (runProgram(K, N)) {
                    left = K;
                } else {
                    right = K;
                }
                break;
            }
        }

        // Итоговое N
        int foundN = left;
        System.out.println("Найденное N = " + foundN);
        System.out.println("Количество сравнений: " + comparisons);
    }
}