import os

import click
from pytubefix import Stream

from samvad.ui.loading_bar import SamvadDownloadFileOverNetworkLoadingBar
from samvad.utils.data import data_root_dir
from samvad.utils.data import download_youtube_video as ydl


@click.command(name="ydl")
@click.option("--url", required=True, help="The URL of the YouTube video to download.")
@click.option(
    "--filename",
    default="video.mp4",
    help="The name of the downloaded video file. It should include the file extension.",
)
@click.option(
    "--res",
    default="480p,360p,720p",
    help="The resolution of the downloaded video. To add fallback resolutions, separate them with commas.",
)
@click.option(
    "--out",
    default=os.path.join(data_root_dir, "raw"),
    help="The output directory for the downloaded video.",
)
def download_youtube_video(url, filename, res, out):
    loading_bar = SamvadDownloadFileOverNetworkLoadingBar("Downloading")
    loading_bar.waiting()

    if not os.path.exists(out):
        os.makedirs(out)

    out_path = os.path.join(out, filename)

    def on_progress(stream: Stream, chunk: bytes, bytes_remaining: int):
        loading_bar.max = stream.filesize
        loading_bar.index = stream.filesize - bytes_remaining
        loading_bar.update_message_prefix(stream.title)
        loading_bar.next(0)

    def on_complete(_, __):
        loading_bar.finish()

    resolutions = res.split(",")

    try:
        stream = ydl(
            url,
            output_path=out,
            filename=filename,
            res_to_download=resolutions[0],
            fallback_resolutions=resolutions[1:],
            on_progress=on_progress,
            on_complete=on_complete,
        )
    except Exception as e:
        print(f"Error: {e}")
        click.secho("\nFailed to download file.", fg="red")
        return

    click.secho(
        f"""\nDownloaded stream info:
itag: {stream.itag}
resolution: {stream.resolution}
fps: {stream.fps}
video_codec: {stream.video_codec}
audio_codec: {stream.audio_codec}
        """,
        fg="blue",
    )
    click.secho(f"""\nSaved video to {out_path}""", fg="green")


@click.group()
def data():
    pass


data.add_command(download_youtube_video)
