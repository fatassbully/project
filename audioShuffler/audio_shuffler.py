import random
import pydub
import os
# v2.1


def slice_n_dice(linktoaudio="", typeofaudio="", shuffle=True, number_of_slices=30, percentage=0, times=1):
    # Changing directory to the directory of audio file
    print('Enter in func QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')


    chislo = 0
    for symbol in linktoaudio[::-1]:

        if symbol == "\\":
            break
        else:
            chislo += 1
    end = len(linktoaudio) - chislo
    fordirectory = linktoaudio[:end]
    print(fordirectory)
    os.chdir(fordirectory)

    # Check for Number of Repeats
    if times < 1:
        times = 1
        print("The number of repeats can't be less than 1")

    # Creating blank list
    list_of_snippets = []

    # Opening file to slice
    if typeofaudio == ".wav":
        file = pydub.AudioSegment.from_wav(linktoaudio)
    elif typeofaudio == ".mp3":
        file = pydub.AudioSegment.from_mp3(linktoaudio)
    else:
        print("Fignia kakaia to")

    # Check if number of slices exceeds the length of file
    if number_of_slices <= file.__len__():
        step = file.__len__() // number_of_slices
    else:
        step = random.choice(range(file.__len__()))

    # Starting point for slicing
    start = 0

    # 'For' cycle that slices the file and puts them in list
    for i in range(number_of_slices):

        snippet = file[start:start+step]
        list_of_snippets.append(snippet)
        start += step

    # Shuffling the resulting list
    if shuffle:
        random.shuffle(list_of_snippets)
    else:
        list_of_snippets = list_of_snippets

    # Creation or opening of Temp File
    if os.path.isfile('Temp.wav'):
        final_file = pydub.AudioSegment.silent(duration=0)
    else:
        s = open('Temp.wav', 'x')
        s.close()
        final_file = pydub.AudioSegment.silent(duration=0)

    # Gluing all back together
    for i in list_of_snippets:
        for j in range(times):
            ran = random.randint(0, 100)
            if ran < percentage:
                final_file += i.reverse()
            else:
                final_file += i

    if typeofaudio == "wav":
        return final_file.export('Result.wav', format='wav'), \
           os.remove('Temp.wav'), \
           print('All good')
    else:
        return final_file.export('Result.mp3', format='mp3'), \
               os.remove('Temp.wav'), \
               print('All good')
