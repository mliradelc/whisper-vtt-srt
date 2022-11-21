import os
import whisper
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE
import argparse
import warnings
from moviepy.editor import VideoFileClip
import sys
from .utils import slugify, str2bool, write_srt, write_vtt
import tempfile


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", nargs="+", type=str,
                        help="video file to transcribe")
    parser.add_argument("--model", default="base",
                        choices=whisper.available_models(), help="name of the Whisper model to use")
    parser.add_argument("--format", default="vtt",
                        choices=["vtt", "srt"], help="the subtitle format to output")
    parser.add_argument("--output_dir", "-o", type=str,
                        default=".", help="directory to save the outputs")
    parser.add_argument("--verbose", type=str2bool, default=False,
                        help="Whether to print out the progress and debug messages")
    parser.add_argument("--task", type=str, default="transcribe", choices=[
                        "transcribe", "translate"], help="whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate')")
    parser.add_argument("--language", type=str, default=None, choices=sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
                        help="language spoken in the audio, skip to perform language detection")

    parser.add_argument("--break-lines", type=int, default=0, 
                        help="Whether to break lines into a bottom-heavy pyramid shape if line length exceeds N characters. 0 disables line breaking.")

    args = parser.parse_args().__dict__
    model_name: str = args.pop("model")
    output_dir: str = args.pop("output_dir")
    subtitles_format: str = args.pop("format")
    os.makedirs(output_dir, exist_ok=True)

    if model_name.endswith(".en"):
        warnings.warn(
            f"{model_name} is an English-only model, forcing English detection.")
        args["language"] = "en"

    videoPath = args.pop("video")[0]
    audio_path = get_audio(videoPath)
    fileTitle = os.path.basename(videoPath)
    break_lines = args.pop("break_lines")

    model = whisper.load_model(model_name)


    warnings.filterwarnings("ignore")

    print (audio_path)
    result = model.transcribe(audio_path, **args)
    warnings.filterwarnings("default")

    if (subtitles_format == 'vtt'):
        vtt_path = os.path.join(output_dir, f"{slugify(fileTitle)}.vtt")
        with open(vtt_path, 'w', encoding="utf-8") as vtt:
            write_vtt(result["segments"], file=vtt, line_length=break_lines)

        print("Saved VTT to", os.path.abspath(vtt_path))
    else:
        srt_path = os.path.join(output_dir, f"{slugify(fileTitle)}.srt")
        with open(srt_path, 'w', encoding="utf-8") as srt:
            write_srt(result["segments"], file=srt, line_length=break_lines)

        print("Saved SRT to", os.path.abspath(srt_path))


def get_audio(videoFile):
    
    temp_dir = tempfile.gettempdir()
    AudioPath = os.path.join(temp_dir, os.path.basename(videoFile)+".mp3")
    clip = VideoFileClip(videoFile)
    clip.audio.write_audiofile(AudioPath)
    

    return AudioPath


if __name__ == '__main__':
    main()
