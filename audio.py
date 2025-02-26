from pydub import AudioSegment
from pydub.generators import Sine
from tqdm import tqdm
import random, string

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----'
}

def generate_morse_code_audio(message, frequency=700, dit_length=60, letter_pause=8*180, word_pause=5*420):
    audio = AudioSegment.silent(duration=10000)
    dit = Sine(frequency).to_audio_segment(duration=dit_length)
    dah = Sine(frequency).to_audio_segment(duration=dit_length*3)
    pause = AudioSegment.silent(duration=dit_length)
    letter_pause = AudioSegment.silent(duration=letter_pause)
    word_pause = AudioSegment.silent(duration=word_pause)

    message = ''.join(char for char in message if char.isalnum()).upper()

    for i, char in enumerate(tqdm(message)):
        for symbol in MORSE_CODE_DICT[char]:
            if symbol == '.':
                audio += dit + pause
            elif symbol == '-':
                audio += dah + pause
        audio += letter_pause
        if (i+1)%4 == 0:
            audio += word_pause

    return audio

if __name__ == "__main__":
    exercise = True # comment out for normal usage
    if exercise:
        message = ''.join(random.choice(string.ascii_uppercase) for _ in range(400))
        print(message)
    else:
        with open("message.txt", "r") as file:
            message = file.read().strip()

    morse_code_audio = generate_morse_code_audio(message)
    morse_code_audio.export("audio.mp3", format="mp3")