from moviepy.editor import *
from pydub import AudioSegment

def convert_to_audio(video_path, audio_path):

    print("Making .mp3 file")
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("output_audio.mp3")
    print("Making .mp3 file - Done")

    # -----------------------------------------------


    # Load MP3 file
    print("Making stereo .wav file")
    audio = AudioSegment.from_mp3('output_audio.mp3')
    # # Convert to WAV
    audio.export("output_audio.wav", format="wav")
    print("Making stereo .wav file - Done")

    #-----------------------------------------------
    # Load audio file
    print("Making mono .wav file")
    audio = AudioSegment.from_wav("output_audio.wav")

    # Convert to mono
    audio = audio.set_channels(1)

    # Set frame rate
    audio = audio.set_frame_rate(16000)

    # Save new audio
    audio.export(audio_path + "output_audio_mono.wav", format="wav")

    print("Making mono .wav file - Done")

