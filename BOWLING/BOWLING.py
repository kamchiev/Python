#JUST NOTES
#number of shots might differ player to player
#same player name is not possible
#print name, surname, score in DESCENDING order of scores
# find players who got more 10's and 0's (format--> name, surname, COUNT of 0's or 10's

try:
    file_in = open('C:\\Users\\khayo\\Desktop\\exam problems\\BOWLING\\bowling.txt')
except (IOError, OSError):
    exit("file path eror")


def main():
    sort = sort_lst(file_in)
    rank = decreasing_rank(sort)
    b = bound(sort)

    for item in rank:
        print(f'{item[2]} {item[1]} {item[0]}') #print (descending ordered list) name, surname, score one by one

    print(f'{b[0][2]} {b[0][1]} has knocked down all the pins {b[0][0]} times') #max 10s
    print(f'{b[1][2]} {b[1][1]} has missed all the pins {b[1][0]} time (s)') #max 0s


def sort_lst(file_name):

    lst = []
    for row in file_name:
        row_split = row.strip('\n').split(';')

        lst_int = []
        for i in range(2, len(row_split)): #scores starts from index 2 --
            convert2int = int(row_split[i]) #-->convert scores to int. other solution: list comprehention
            lst_int.append(convert2int)

        lst.append([row_split[1], row_split[0], lst_int]) #[[name,surname,[scores]],...

    return lst


def decreasing_rank(infos):

    ranking_list = []

    for items in infos:
        ranking_list.append([sum(items[2]), items[0], items[1]]) #sum scores [[SCORE, name, surname],...

    return sorted(ranking_list, reverse=True) #sort it descending order


def bound(infos):

    max_10s = []
    max_0s = []

    for items in infos:
        count10s = 0
        count0s = 0

        for element in items[2]:
            if element == 10:
                count10s += 1
            if element == 0:
                count0s += 1

        max_10s.append([count10s, items[0], items[1]]) #[[max 0's, name, surname],...
        max_0s.append([count0s, items[0], items[1]]) ##[[max 10's, name, surname],...

    return max(max_10s), max(max_0s) #find element with max number


main()

file_in.close()
