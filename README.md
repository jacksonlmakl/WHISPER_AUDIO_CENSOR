# Audio Censoring Project

This project provides a tool for censoring specified "bad words" in an audio file using OpenAI's Whisper model for transcription and PyDub for audio manipulation. It includes a Flask app for easy uploading and processing of audio files through a web interface.

## Features

- Transcription of audio files to text using OpenAI's Whisper model.
- Identification and censoring of specified bad words in the audio file.
- A simple web interface for uploading audio files and specifying bad words to censor.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher installed.
- Flask installed for the web app functionality.
- OpenAI API key for using the Whisper model.
- All required Python libraries installed (use `requirements.txt`).

## Installation

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY='your_api_key_here'
    ```

## Usage

### Running the Flask App

1. Start the Flask app:

    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Use the web interface to upload an audio file and input the bad words you want to censor, separated by commas.

4. Click on "Upload and Censor" to process the file. The censored audio file will be automatically downloaded once the processing is complete.

### Using the Audio Censoring Script Directly

To directly use the audio censoring script without the Flask app:

1. Ensure you are in the project's root directory.

2. Run the script with the required arguments:

    ```bash
    python main_bulk.py --file_path="path/to/your/audio.mp3" --bad_words="word1,word2,word3"
    ```

    Replace `path/to/your/audio.mp3` with the path to your audio file and `"word1,word2,word3"` with the words you want to censor.

## Configuration

- To change the sensitivity of silence detection or chunk sizes, edit the `split_audio` function parameters in `censor_audio.py`.
- Adjust the sine wave frequency for the censor beep in the `censor_chunk` function.

## Contributing

We welcome contributions! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

If you have any questions or feedback, please contact me at your-email@example.com.
