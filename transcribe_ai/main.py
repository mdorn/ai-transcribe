
import logging
import os
from pathlib import Path

from tqdm import tqdm
from openai import OpenAI

logging.basicConfig()
logger = logging.getLogger('AITranscribe')
logger.setLevel(logging.INFO)

client = OpenAI()

# Define the path to the directory containing audio files
# path = "/Users/mdorn/Desktop/Oblates Formation Podcasts"
# path = '/tmp/test'

def transcribe(path):
    """
    Transcribes the audio file at the given path using OpenAI's Whisper model.
    
    Args:
        path (str): The path to the audio file.
    
    Returns:
        dict: The transcription result.
    """
    transcript = client.audio.transcriptions.create(model="whisper-1", file=path)
    return transcript

def write_transcript_with_paragraphs(fileobj, transcript):
    """
    Formats the transcript by inserting paragraph breaks and writes it to a markdown file.
    
    Args:
        fileobj (os.DirEntry): The file object representing the audio file.
        transcript (dict): The transcription result.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert writer and editor, versed in English grammar."},
            {"role": "user", "content": f"Insert paragraph breaks at logical points into the following text:\n\n{transcript.text}"}
        ]
    )
    output = response.choices[0].message.content
    output_filename = '{}.md'.format(Path(fileobj.name).stem)
    output_filepath = os.path.join(os.path.dirname(fileobj.path), output_filename)
    
    # Write the formatted transcript to a markdown file
    with open(output_filepath, 'w') as output_file:
        output_file.write(output)

def process_files(path):
    """
    Processes all .mp3 files in the given directory, transcribing and formatting each one.
    
    Args:
        path (str): The path to the directory containing audio files.
    """
    logger.info('Processing files at {}'.format(path))
    with os.scandir(path) as file_list:
        # Filter for .mp3 files
        files = [f for f in file_list if f.name.endswith('.mp3')]
        
        # Process each file with a progress bar
        for name in tqdm(files):
            transcript = transcribe(name)
            write_transcript_with_paragraphs(name, transcript)
