import os
import random
import pydub
# v2.2


def slice_n_dice(link_to_audio="", shuffle=True, number_of_slices=30, percentage=0, times=1):

    try:
        type_of_audio = pydub.utils.mediainfo(link_to_audio)['codec_name']
    except BaseException:
        raise BaseException('I can not get the file')

    # Changing directory to the directory of audio file
    for_directory = os.path.dirname(link_to_audio)
    os.chdir(for_directory)

    # Check for Number of Repeats
    if times < 1:
        print("The number of repeats can't be less than 1.")
        print("Setting the number to 1.")

    # Creating blank list
    list_of_snippets = []

    # Opening file to slice
    wav_formats = ("wav","pcm_s8le","pcm_s16le","pcm_s24le","pcm_s32le")

    if type_of_audio in wav_formats:
        audio = pydub.AudioSegment.from_wav(link_to_audio)
    elif type_of_audio == "mp3":
        print("MP3")
        audio = pydub.AudioSegment.from_mp3(link_to_audio)
    else:
        final_file = pydub.AudioSegment.from_mp3("K:\Python_Courses\Wav_shuffler\Error.mp3")
        return final_file.export('Result.mp3', format='mp3'), True




    # Check if number of slices exceeds the length of file
    audio_length = len(audio)
    if number_of_slices <= audio_length:
        step = audio_length // number_of_slices
    else:
        step = random.choice(range(audio_length))

    # Starting point for slicing
    start = 0

    # 'For' cycle that slices the file and puts them in list
    for i in range(number_of_slices):

        snippet = audio[start:start+step]
        list_of_snippets.append(snippet)
        start += step

    # Shuffling the resulting list
    if shuffle:
        random.shuffle(list_of_snippets)
    else:
        pass

    # Creation of Final File
    final_file = pydub.AudioSegment.silent(duration=0)

    # Gluing all back together
    for i in list_of_snippets:
        for j in range(times):
            ran = random.randint(0, 100)
            if ran < percentage:
                final_file += i.reverse()
            else:
                final_file += i

    if type_of_audio == "wav":
        final_file.export('Result.mp3', format='wav')
        return True
    else:
        final_file.export('Result.mp3', format='mp3')
        return True


slice_n_dice("K:\Python_Courses\Wav_shuffler\\voice.wav", True, 50, 50, 5)
