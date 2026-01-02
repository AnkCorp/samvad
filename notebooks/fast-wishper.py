import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import moviepy
    from faster_whisper import WhisperModel

    notebook_path = os.path.abspath(os.path.join(".", "notebooks"))
    mp4_path = os.path.join(notebook_path, "4.mp4")
    mp3_out_path = os.path.join(notebook_path, "1.mp3")
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
def _(model, mp4_path):
    segments, info = model.transcribe(mp4_path, word_timestamps=True,      vad_parameters=dict(min_silence_duration_ms=2000,vad_filter=True)
    )
    return (segments,)


@app.cell
def _(segments):
    segments
    return


@app.cell
def _():
    import time

    def seconds_to_srt_time(seconds):
        """
        Converts a float or int representing seconds into SRT time format (HH:MM:SS,mmm).

        The time.gmtime() method works well within a 24-hour cycle (up to 86400 seconds).
        If the time exceeds 24 hours, the hours will wrap around (e.g., 25 hours becomes 01:00:00).
        """
        # Separate the integer seconds from the fractional milliseconds
        # strftime does not handle fractions of a second (milliseconds)
        # The snippet uses time.gmtime() and string formatting for this.
        try:
            # Get integer seconds and remaining milliseconds
            int_seconds = int(seconds)
            milliseconds = int(round((seconds - int_seconds) * 1000))

            # Adjust if rounding pushed milliseconds to 1000
            if milliseconds == 1000:
                int_seconds += 1
                milliseconds = 0

            # Format the time part (HH:MM:SS) using time.strftime and time.gmtime
            # Note: gmtime wraps around after 24 hours (86400 seconds)
            time_part = time.strftime("%H:%M:%S", time.gmtime(int_seconds))

            # Combine the time part with the formatted milliseconds
            srt_time = f"{time_part},{milliseconds:03d}"

            return srt_time

        except (ValueError, OverflowError, TypeError):
            return "Invalid input"
    return (seconds_to_srt_time,)


@app.cell
def _(seconds_to_srt_time, segments):
    out = ""
    idx = 1
    for segment in segments:
        out += f"""
    {idx}
    {seconds_to_srt_time(segment.start)} --> {seconds_to_srt_time(segment.end)}
    {segment.text}
    """
        print(out)
        idx += 1



    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(
            out,
        )
    return (out,)


@app.cell
def _():
    import srt
    return (srt,)


@app.cell
def _(out, srt):
    subs = list(srt.parse(out))
    subs[0].content
    return (subs,)


@app.cell
def _(subs):
    sentences = []
    current_sentence = ""
    total = len(subs)
    for index, sub in enumerate(subs):
        is_last = index + 1 >= total
        if is_last or sub.content[-1] == "." and (subs[index + 1].start - sub.end).total_seconds() > 0.2:
            sentences.append(f"{current_sentence} {sub.content}".strip())
            current_sentence = ""
            continue
        current_sentence = f"{current_sentence} {sub.content}"

    sentences
    return


@app.cell
def _(re):
    print(re.search('([A-Z]\.){2,}', "H.R.D.F.M."))
    return


@app.cell
def _(subs):
    a = subs[6].start - subs[5].end
    a.total_seconds()
    return


if __name__ == "__main__":
    app.run()
