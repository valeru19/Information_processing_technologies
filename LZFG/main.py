from math import log2, ceil

x1 = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
x2 = "early_to_bed_and_early_to_rise_makes_a_man_wise"
x3 = "can_you_can_a_can_as_a_canner_can_can_a_can?"

def match_lenght(string, substring):
    total = 0
    for i in range(len(substring)):
        buffer = ''
        for j in range(i, len(substring)):
            buffer += substring[j]
            if not (buffer in string):
                break
            if total < len(buffer):
                total = len(buffer)
    if total < 3 and total != 0:
        return str(total) + "(<3)"
    return total

def bin_quad_len(lenght):
    binary = bin(lenght)[2:]
    zeros_len = 4-len(binary)
    return "0"*zeros_len+binary

def bin_adaptive_len(d, window_len):
    lenght = ceil(log2(window_len))
    binary = bin(d)[2:]
    zeros_len = lenght - len(binary)
    return "0"*zeros_len+binary

def bin_for_string(char):
    bytes_data = char.encode('utf-8')
    binary_code = ' '.join(format(byte, '08b') for byte in bytes_data)
    return binary_code

def LZFG(x):
    N = 0
    n = len(x)
    c = ''
    step = 0
    binaries = []
    bin_sum = 0

    print(
        f"{'Шаг':<8}"
        f"{'Длина совпад.':<18}"
        f"{'Расстояние до обр.':<22}"
        f"{'Кол-во новых букв':<22}"
        f"{'Код. символы':<23}" 
        f"{'Переданные слова':<20}"
        f"{'Затраты (бит)':<12}"
    )

    while N < n:
        l = 3
        if x[N:N+l] in c:
            while l < 17 and x[N:N+l+1] in c and N+l+1 <= n:
                l += 1
            d = N - c.rindex(x[N:N + l]) - 1 # расстояние до образца

            binary = bin_quad_len(l - 2)+" "+bin_adaptive_len(d, len(c))
            binaries.append(binary)
            bin_sum += len(binary) - 1

            step += 1
            print(
                f"{str(step).ljust(8)}"
                f"{str(match_lenght(c,x[N:N+l])).ljust(18)}"
                f"{str(d) + '(' + str(N) + ')':<22}"
                f"{'—':<22}"
                f"{binary.ljust(23)}"
                f"{x[N:N+l].ljust(20)}"
                f"{str(len(binary) - 1).rjust(12)}"
            )
            c += x[N:N+l]
            N += l
        else:
            L = 0
            j = ''
            while L < 16 and not(x[N:N+3] in c) and not(x[N:N+3] in j):
                j += x[N]
                N += 1
                L += 1

            binary = "0000 "+bin_quad_len(L - 1)
            binaries.append(binary+" "+bin_for_string(j))
            bin_sum += 8 + 8 * len(j)

            step += 1
            print(
                f"{str(step).ljust(8)}"
                f"{str(match_lenght(c, j)).ljust(18)}"
                f"{'—'.ljust(22)}"
                f"{str(len(j)).ljust(22)}"
                f"{(binary+' bin(...)').ljust(23)}"
                f"{str(j).ljust(20)}"
                f"{str(8 + 8 * len(j)).rjust(12)}"
            )
            c += j
    print(f'Итого{str(bin_sum).rjust(120  )}\n')

    print(f"{'Шаг':<5} Код. символы")
    for i in range(len(binaries)):
        print(f'{i + 1:<5} {binaries[i]}')

LZFG(x1)

