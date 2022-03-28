#JUST NOTES
# let's create list that contains [year,name of album, code of singer]
# then create an empty dictionary, loop over list and if key equal to year, add it as a one of the element of values
# like 1985 : [[song1, singer code],[song2, singer code] ...]
## album of singers and songs in that albums are given. print name of song and its code ascending order of year

try:
    file_artists = open('C:\\Users\\khayo\\Desktop\\exam problems\\DISCOGRAFIA\\artists.txt')
except (IOError,OSError):
    exit("file path eror")

def main():
    full_list = sorted(make_full_list(file_artists)) #sort that list with year

    lst = set()      #we need same year only one time
    for items in full_list:
        if items[0] not in lst:
            lst.add(items[0])
            print(f'{items[0]}:') #we only print year if it has not printed already.
        print(f'{items[1]} {items[2]}')
        

def make_full_list(file_name):

    lst_all = []
    for row in file_name: #read file line by line
        singer_albums = row.split(';')[1].strip('\n') #taking only name of albums
        try:
            file_albums = open(f'C:\\Users\\khayo\\Desktop\\exam problems\\DISCOGRAFIA\\{singer_albums}')
        except (IOError, OSError):
            exit("file path eror")
        #open all albums one by one

        for songs in file_albums: #itarate over albums
            songs_split = songs.split(';') #split it by ;

            lst_all.append([songs_split[0], songs_split[1].strip('\n'), row.split(';')[0]])
            #[[year, song name, song code] ... (here we put all songs in one list)

    return lst_all


main()

file_artists.close()
