# WhisperSubs
Automatic Whisper subtitle generation

This repository uses [OpenAI's Whisper](https://openai.com/blog/whisper) to generate subtitle files for any video.

It would be useful to add here what this fork provides that the native whisper .vtt and .srt output does not. Do you have better break lengths, better handling of pauses in speaking, or improvements on display duration due to your process of converting the timestamps and words into vtt and srt segments?

## Installation

To get started, you'll need Python 3.7 or newer. Install the binary by running the following command:

    pip install git+https://github.com/maxlira/whisper-vtt-srt

You'll also need to install [`ffmpeg`](https://ffmpeg.org/), which is available from most package managers:

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg
```

## Usage

The following command will generate a VTT file from the specified video

    subs_whisper <video-file>
    
The default setting (which selects the `base` model) works well for transcribing most languages. You can optionally use a bigger model for better results (especially with other languages). The available models are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`.

    subs_whisper <video-file> --model medium

Adding `--task translate` will translate the subtitles into English:

    subs_whisper <video-file> --task translate

Run the following to view all available options:

    subs_whisper --help

## License

This script is open-source and licensed under the MIT License. For more details, check the [LICENSE](LICENSE) file.
