Transcribe .mp3 files in a given directory using OpenAI's Whisper model, and insert paragraph breaks using GPT.

Usage after cloning repo and installing requirements:

```bash
export OPENAI_API_KEY=...
export PYTHONPATH=.
python transcribe_ai/cli.py /path/to/mp3/files
```