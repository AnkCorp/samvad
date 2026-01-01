import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import moviepy
    from faster_whisper import WhisperModel

    notebook_path = os.path.abspath(os.path.join(".", "notebooks"))
    mp4_path = os.path.join(notebook_path, "2.mp4")
    mp3_out_path = os.path.join(notebook_path, "2.mp3")
    return WhisperModel, moviepy, mp3_out_path, mp4_path


@app.cell
def _(moviepy, mp4_path):
    video = moviepy.VideoFileClip(mp4_path)
    return (video,)


@app.cell
def _(mp3_out_path, video):
    video.audio.write_audiofile(mp3_out_path)
    return


@app.cell
def _(moviepy, mp3_out_path):
    audio = moviepy.AudioFileClip(mp3_out_path)
    return


@app.cell
def _(WhisperModel):
    model = WhisperModel("small", device="cuda", compute_type="float16")
    return (model,)


@app.cell
def _(model, mp3_out_path):
    segments, info = model.transcribe(mp3_out_path)
    print("Transcription language", info[0])
    return info, segments


@app.cell
def _(segments):
    segments
    return


@app.cell
def _(info, segments):
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return


if __name__ == "__main__":
    app.run()
