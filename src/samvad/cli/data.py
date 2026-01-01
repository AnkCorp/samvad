import os

import click
from pytubefix import Stream

from samvad.ui.loading_bar import SamvadDownloadFileOverNetworkLoadingBar
from samvad.utils.data import data_root_dir
from samvad.utils.data import download_youtube_video as ydl
from samvad.utils.path import ensure_dir


def _print_stream_info(stream: Stream) -> None:
    """Print detailed information about the downloaded stream."""
    click.secho(
        f"""\nStream info:
itag: {stream.itag}
resolution: {stream.resolution}
fps: {stream.fps}
video_codec: {stream.video_codec}
audio_codec: {stream.audio_codec}
        """,
        fg="blue",
    )


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
    """Download a YouTube video with optional resolution fallbacks."""
    ensure_dir(out)

    loading_bar = SamvadDownloadFileOverNetworkLoadingBar("Downloading")
    loading_bar.waiting()

    def _progress_callback(stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
        loading_bar.max = stream.filesize
        loading_bar.index = stream.filesize - bytes_remaining
        loading_bar.update_message_prefix(stream.title)
        loading_bar.next(0)

    def _complete_callback(_, __) -> None:
        loading_bar.finish()

    resolutions = [r.strip() for r in res.split(",") if r.strip()]
    primary_res, fallback_res = resolutions[0], resolutions[1:]

    try:
        stream = ydl(
            url,
            output_path=out,
            filename=filename,
            res_to_download=primary_res,
            fallback_resolutions=fallback_res,
            on_progress=_progress_callback,
            on_complete=_complete_callback,
        )
    except Exception as e:  # pragma: no cover
        click.secho(f"\nFailed to download file: {e}", fg="red")
        return

    _print_stream_info(stream)
    click.secho(f"\nSaved video to {os.path.join(out, filename)}", fg="green")


@click.group()
def data():
    pass


data.add_command(download_youtube_video)
