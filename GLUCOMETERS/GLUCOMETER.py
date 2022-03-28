#exceeding level 200
#chronological order and missing measurements may occur
# format: [ID, acquisition time, blood glucose value, body temperature, heart rate]

file_path = 'C:\\Users\\khayo\\Desktop\\exam problems\\GLUCOMETERS\\glucometers.txt'


def main():
    read = read_file(file_path)
    sol = solution(read)

    p_set = set()
    p_set.add(sol[0][0])
    for i in sol:
        if i[0] not in p_set:
            p_set.add(i[0])
            print()
        print(f'{i[0]} {i[1]} {i[2]}')


def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_data = f.read().split('\n')
    except (IOError, OSError):
        print("such file is not found")
        exit()
    return sorted(file_data)


def solution(data):
    lst = []
    for row in data:
        r_s = row.split()

        if int(r_s[2]) >= 200:
            lst.append(r_s)

    return lst


main()
