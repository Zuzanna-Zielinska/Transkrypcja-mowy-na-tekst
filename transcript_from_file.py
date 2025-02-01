import json
import wave
from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel
SetLogLevel(-1)
from convert_to_audio import convert_to_audio
import os
import math
from tqdm import trange

def make_transcript(video_folder_path = "video", transcript_folder_path = 'transcripts'):

    model = Model(r"vosk-model")
    rec = KaldiRecognizer(model, 16000)

    number_of_farmes = 30

    for name in os.listdir(video_folder_path):

        print("-------------------------------------------------------")
        print(f"Transcribing {name[:-4]}")

        convert_to_audio('video/' + name, '')

        # Open WAV file
        wf = wave.open("output_audio_mono.wav", "rb")
        seconds = wf.getnframes() / wf.getframerate()
        batch_size = math.ceil(len(wf.readframes(99999999999999999999999999999999999999999))/number_of_farmes)
        batch_size = batch_size//2

        # List to hold all text segments
        transcribed_text_list = []

        print("Making transcription\n")

        time = 0

        wf = wave.open("output_audio_mono.wav", "rb")
        for i in trange(batch_size):
            time += seconds/batch_size

            data = wf.readframes(number_of_farmes)

            # print(f"Frame {i+1}/{batch_size} - {i/batch_size*100}%")

            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())

                transcribed_text_list.append(f'[{int(time//3600)}:{int(time//60)}:{int(time%60)}] {result["text"]}')
                transcribed_text_list.append('\n')

        # Handle last part of audio
        final_result = json.loads(rec.FinalResult())
        transcribed_text_list.append(final_result['text'])

        # Concatenate all text segments
        complete_text = ' '.join(transcribed_text_list)

        # Write the complete transcribed text to a text file
        with open(f'{transcript_folder_path}/' + name[:-4] + '.txt', 'w') as f:
            f.write(complete_text)

        print("Making transcription - Done")

if __name__ == '__main__':
    make_transcript()
