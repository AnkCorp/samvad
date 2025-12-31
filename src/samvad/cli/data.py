import click


@click.command(name="download")
def download_data():
    print("Download data from somewhere...")


@click.group()
def data():
    pass


data.add_command(download_data)
