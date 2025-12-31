import os
from typing import Any, Callable, Optional

from pytubefix import Stream, YouTube

data_root_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "__data__")
)


def download_youtube_video(
    url: str,
    output_path: str,
    filename: str,
    res_to_download: str,
    fallback_resolutions: list[str] = [],
    on_progress: Optional[Callable[[Stream, bytes, int], None]] = None,
    on_complete: Optional[Callable[[Any, Optional[str]], None]] = None,
) -> Stream:
    """
    Download a YouTube video.

    Args

        url (str):
            The URL of the YouTube video to download.

        output_path (str):
            The path where the downloaded video will be saved.

        filename (str):
            The name of the downloaded video file. It should include the file extension.

        res_to_download (str):
            The desired resolution of the video. If not available, the function will attempt
            to find a suitable fallback resolution.

        fallback_resolutions (list[str], optional):
            A list of fallback resolutions in descending order of preference.

        on_progress (Optional[Callable[[Stream, bytes, int], None]], optional):
            A callback function that will be called periodically during the download process.

        on_complete (Optional[Callable[[Any, Optional[str]], None]], optional):
            A callback function that will be called once the download is complete.

    Raises:
        ValueError: If the specified resolution is not available and no fallback resolutions are provided.
        Exception: If any other error occurs during the download process.
    """

    yt = YouTube(url)

    resolutions = [res_to_download, *fallback_resolutions]
    stream = None
    for res in resolutions:
        stream = yt.streams.filter(
            res=res, type="video", audio_codec="mp4a.40.2"
        ).first()
        if stream is not None:
            break

    if stream is None:
        raise ValueError(
            f"None of the specified resolutions ({', '.join(resolutions)}) are available."
        )

    if on_progress is not None:
        yt.register_on_progress_callback(on_progress)

    if on_complete is not None:
        yt.register_on_complete_callback(on_complete)

    stream.download(output_path, filename)

    return stream
