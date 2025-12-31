from humanize import naturalsize, time
from progress.bar import Bar


class SamvadDownloadFileOverNetworkLoadingBar(Bar):
    """A util class for file download progress bar"""

    fill = "+"
    empty_fill = "-"
    suffix = "%(percent).1f%% %(eta_download)s"
    waiting_bar = Bar()

    def __init__(self, message="", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

        self.waiting_bar = Bar(
            fill=self.empty_fill,
            empty_fill=self.empty_fill,
            suffix="0%% (loading...)",
        )

        self.update_message_prefix(message)

    def update_message_prefix(self, message):
        msg = message[:20]

        if len(message) > 20:
            msg += "..."
        self.message = f"{msg} %(file_downloaded_status)s"
        self.waiting_bar.message = f"{msg} [-/-]"

    @property
    def file_downloaded_status(self):
        if self.max == 0 or self.index == 0:
            return "-/-"

        return f"[{naturalsize(self.index)}/{naturalsize(self.max)}]"

    @property
    def eta_download(self):
        if self.elapsed < 5:
            # At least wait for 5 seconds before showing eta
            return ""

        return f"({time.naturaldelta(self.eta)} left)"

    def waiting(self):
        return self.waiting_bar.next()
