import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from pytubefix import YouTube
    from progress.bar import Bar
    return (YouTube,)


@app.cell
def _(YouTube):
    yt = YouTube("https://www.youtube.com/watch?v=sU1YgEjPavs")
    yt.streams
    return (yt,)


@app.cell
def _(yt):
    yt.streams.filter(type="video", res="720p")
    return


app._unparsable_cell(
    r"""
    s = next(yt.streams.filter(res=res).first() for res in ['480p', '360p', '720p'])
    print(\"stream\" s

    """,
    name="_"
)


@app.cell
def _(yt):
    # yt.captions['en-GB'].generate_srt_captions()
    yt.captions
    return


@app.cell
def _(yt):
    def on_progress(stream, chunk, bytes_remaining):
        total = stream.filesize
        print(total)
        percent = (1 - bytes_remaining / total) * 100

    def on_complete(stream, file_path):
        print(f"\n√ Done downloading: {file_path}")

    yt.register_on_progress_callback(on_progress)
    yt.register_on_complete_callback(on_complete)

    # 136 -> 720p
    stream = yt.streams.get_by_itag(18)
    return (stream,)


@app.cell
def _(stream):
    stream.download(filename="test.mp4")
    return


@app.cell
def _():
    from progress.bar import IncrementalBar
    import time
    import marimo as mo


    mylist = [1, 2]
    bar = IncrementalBar(max=len(mylist))

    # for item in mylist:
    #     bar.next()
    #     time.sleep(1)
    # bar.finish()

    with mo.status.progress_bar(total = 10, title="Downloading some file", subtitle="Please wait...",show_rate=False) as bar:
        for i in range(10):
            bar.update()
            time.sleep(1)
    return (mo,)


@app.cell
def _(mo):
    mo.running_in_notebook()
    return


@app.cell
def _():
    import humanize
    return (humanize,)


@app.cell
def _(humanize):
    humanize.naturalsize(107725506)

    return


@app.cell
def _(humanize):
    humanize.time.naturaldelta(10)
    return


@app.cell
def _():
    a = "Downloading"
    a = ""

    b = a.split(",")
    b[1:]
    return


@app.cell
def _():
    import torch
    return (torch,)


@app.cell
def _(torch):
    print(torch.version.cuda)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
