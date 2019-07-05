import argparse
import io
from pydub import AudioSegment
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
client = speech.SpeechClient()
#credential_path ="servisentimen-servi
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

###ffmeg



# [START speech_transcribe_async]
def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    # [START speech_python_migration_async_request]
    transcript=""
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
    sound = AudioSegment.from_mp3(content)
    sound.export(speech_file.split('.')[0]+".wav", format="wav")
    with io.open(speech_file.split('.')[0]+".wav", 'rb') as audio_file:
        content2 = audio_file.read()    
    audio = types.RecognitionAudio(content=content2)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='es-CO')        
    # [START speech_python_migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END speech_python_migration_async_request]
    ##print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript
transcribe_file("some.mp3")