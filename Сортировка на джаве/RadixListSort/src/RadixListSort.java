import java.util.Arrays;
import java.util.Scanner;
import java.util.Random;

public class RadixListSort {

    // Структура узла односвязного списка для хранения элементов
    static class Node {
        int[] key;   // Массив цифр, представляющий ключ элемента
        Node next;   // Ссылка на следующий узел в списке

        // Конструктор узла
        Node(int[] key) {
            this.key = key;
            this.next = null;
        }
    }
    static int M; // Основание системы счисления (количество возможных значений цифры, например, 10 для десятичной системы)
    static int p; // Количество разрядов в ключах элементов

    static Node[] TOP;   // Массив указателей на начало каждой корзины
    static Node[] BOTM;  // Массив указателей на конец каждой корзины

    // Выполняет поразрядную сортировку односвязного списка с выводом каждой итерации
    public static void radixSort(Node head) {
        // Проходим по разрядам справа налево (от младшего к старшему)
        for (int k = p - 1; k >= 0; k--) {
            clearBuckets(); // Очищаем корзины перед распределением
            Node R = head; // Указатель на текущий узел списка
            // Распределяем узлы по корзинам в зависимости от цифры в текущем разряде
            while (R != null) {
                int digit = R.key[k]; // Извлекаем цифру в k-м разряде ключа

                // Если корзина пуста, узел становится началом и концом корзины
                if (TOP[digit] == null) {
                    TOP[digit] = BOTM[digit] = R;
                } else {
                    // Иначе добавляем узел в конец корзины
                    BOTM[digit].next = R;
                    BOTM[digit] = R;
                }

                R = R.next; // Переходим к следующему узлу
            }
            head = collectBuckets(); // Собираем узлы из корзин в новый список

            // Выводим состояние списка после обработки текущего разряда
            System.out.print("Итерация " + (p - k) + " (разряд " + (p - k - 1) + "): ");
            printList(head);
        }

        // Выводим окончательный отсортированный список
        System.out.println("Отсортированный список:");
        printList(head);
    }

    // Очищает корзины, сбрасывая указатели TOP и BOTM
    private static void clearBuckets() {
        for (int i = 0; i < M; i++) {
            TOP[i] = null;
            BOTM[i] = null;
        }
    }

    // Собирает узлы из корзин в новый односвязный список
    private static Node collectBuckets() {
        Node newHead = null; // Указатель на начало нового списка
        Node last = null;    // Указатель на последний узел в новом списке

        // Проходим по всем корзинам
        for (int i = 0; i < M; i++) {
            if (TOP[i] != null) {
                // Если корзина не пуста, добавляем её содержимое в список
                if (newHead == null) {
                    newHead = TOP[i]; // Первая корзина становится началом списка
                } else {
                    last.next = TOP[i]; // Связываем с предыдущей корзиной
                }
                last = BOTM[i]; // Обновляем указатель на последний узел
            }
        }
        if (last != null) {
            last.next = null; // Устанавливаем конец списка
        }
        return newHead; // Возвращаем начало нового списка
    }

    // Выводит односвязный список в консоль
    private static void printList(Node head) {
        Node temp = head;
        while (temp != null) {
            System.out.print(Arrays.toString(temp.key) + " "); // Выводим ключ узла
            temp = temp.next; // Переходим к следующему узлу
        }
        System.out.println();
    }

    // Генерирует случайный односвязный список из n элементов
    private static Node generateRandomList(int n, Random rand) {
        Node head = null; // Указатель на начало списка
        Node tail = null; // Указатель на конец списка

        // Создаем n узлов
        for (int i = 0; i < n; i++) {
            int[] key = new int[p]; // Создаем ключ из p цифр
            for (int j = 0; j < p; j++) {
                key[j] = rand.nextInt(M); // Генерируем случайную цифру от 0 до M-1
            }

            Node newNode = new Node(key); // Создаем новый узел
            if (head == null) {
                head = tail = newNode; // Если список пуст, узел становится началом
            } else {
                tail.next = newNode; // Добавляем узел в конец списка
                tail = newNode; // Обновляем указатель на конец
            }
        }
        return head; // Возвращаем начало списка
    }

    // Создает односвязный список на основе ручного ввода пользователя
    private static Node inputListManually(Scanner scanner) {
        System.out.print("Введите количество элементов для сортировки: ");
        int n = scanner.nextInt();

        Node head = null; // Указатель на начало списка
        Node tail = null; // Указатель на конец списка

        System.out.println("Введите элементы (каждый элемент — " + p + " цифр через пробел):");
        for (int i = 0; i < n; i++) {
            int[] key = new int[p]; // Создаем ключ из p цифр
            System.out.print("Элемент " + (i+1) + ": ");
            for (int j = 0; j < p; j++) {
                while (true) {
                    key[j] = scanner.nextInt(); // Считываем цифру
                    if (key[j] >= 0 && key[j] < M) {
                        break; // Цифра корректна, выходим из цикла
                    }
                    System.out.println("Ошибка! Цифра должна быть от 0 до " + (M-1) + ". Введите снова:");
                }
            }

            Node newNode = new Node(key); // Создаем новый узел
            if (head == null) {
                head = tail = newNode; // Если список пуст, узел становится началом
            } else {
                tail.next = newNode; // Добавляем узел в конец списка
                tail = newNode; // Обновляем указатель на конец
            }
        }
        return head; // Возвращаем начало списка
    }

    // Основной метод программы
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random rand = new Random();

        // Запрашиваем параметры сортировки
        System.out.print("Введите основание системы счисления (M): ");
        M = scanner.nextInt();

        System.out.print("Введите количество разрядов (p): ");
        p = scanner.nextInt();

        // Инициализируем массивы для корзин
        TOP = new Node[M];
        BOTM = new Node[M];

        // Запрашиваем способ ввода данных
        System.out.println("\nВыберите способ ввода данных:");
        System.out.println("1 - Ввести данные вручную");
        System.out.println("2 - Сгенерировать случайные - Сгенерировать случайные данные");
        System.out.print("Ваш выбор: ");

        int choice = scanner.nextInt();
        Node head = null;

        switch (choice) {
            case 1:
                head = inputListManually(scanner); // Создаем список на основе ручного ввода
                break;
            case 2:
                System.out.print("Сколько элементов сгенерировать? ");
                int n = scanner.nextInt();
                head = generateRandomList(n, rand); // Генерируем случайный список
                System.out.println("\nСгенерированный список:");
                printList(head);
                break;
            default:
                System.out.println("Неверный выбор. Программа завершена.");
                System.exit(0);
        }

        System.out.println("\nДо сортировки:");
        printList(head);

        System.out.println("\nПроцесс поразрядной сортировки:");
        radixSort(head);

        scanner.close(); // Закрываем сканнер
    }
}