import os
from openai import OpenAI
from pydub import AudioSegment, silence
from pydub.generators import Sine

def get_word_data(file_path):
  client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
  )
  audio_file= open(file_path, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format='verbose_json',
    timestamp_granularities=["word"]
  )
  return transcription.words

def get_bad_words(word_data,bad_words):
  for i in word_data:
    for bad_word in bad_words:
      if bad_word.lower() in i['word'].lower():
        start=i['start']
        end=i['end']
        if start>0:
            start=start-.02
        yield (start,end)
        continue


def split_audio(file_path, chunk_length_ms=300000):  # 5 minutes in milliseconds
    """Splits the audio file into chunks of the specified length."""
    audio = AudioSegment.from_mp3(file_path)
    chunks = silence.split_on_silence(audio, min_silence_len=2000, silence_thresh=-40, keep_silence=500)

    # Further split if any chunk is longer than the chunk_length_ms
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_length_ms:
            num_subchunks = len(chunk) // chunk_length_ms + 1
            for i in range(num_subchunks):
                start_ms = i * chunk_length_ms
                end_ms = min((i + 1) * chunk_length_ms, len(chunk))
                final_chunks.append(chunk[start_ms:end_ms])
        else:
            final_chunks.append(chunk)
    return final_chunks


def censor_chunk(chunk, censor_intervals):
    """Censors given intervals within a single audio chunk."""
    beep = Sine(1000).to_audio_segment(duration=1000)  # 1 second of beep
    censored_chunk = chunk
    for start, end in censor_intervals:
        start_ms, end_ms = int(start * 1000), int(end * 1000)
        beep_duration = end_ms - start_ms
        beep_sound = beep[:beep_duration]
        censored_chunk = censored_chunk.overlay(beep_sound, position=start_ms, gain_during_overlay=-30)
    return censored_chunk


def censor_audio(file_path, censor_intervals, chunk_length_ms=300000):
    """Splits the audio file, censors each chunk, and concatenates them back."""
    chunks = split_audio(file_path, chunk_length_ms)
    censored_chunks = []

    for chunk in chunks:
        # Adjust intervals for the current chunk
        chunk_intervals = [(start, end) for start, end in censor_intervals if start * 1000 < len(chunk)]
        censored_chunk = censor_chunk(chunk, chunk_intervals)
        censored_chunks.append(censored_chunk)

    # Concatenate all censored chunks
    censored_audio = sum(censored_chunks)

    # Save the censored audio file
    output_path = f"{file_path.replace('.','_')}__censored_audio.mp3"
    censored_audio.export(output_path, format="mp3")
    print(f"Censored audio saved to {output_path}")
    return output_path


def main(file_path, bad_words):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.environ["PATH"] += os.pathsep + current_directory
    word_data = get_word_data(file_path)
    bad_word_data = [i for i in get_bad_words(word_data, bad_words)]
    output_path=censor_audio(file_path, bad_word_data)
    return output_path


if __name__ == "__main__":
    file_path = "wap.mp3"
    bad_words = ["fuck", "pussy", "hoe", "puss", "nigga", "ass", "whore", "shit", "dick"]
    main(file_path=file_path, bad_words=bad_words)
