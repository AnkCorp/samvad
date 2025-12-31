import click

from samvad.cli.data import data


@click.group()
def main():
    pass


main.add_command(data)
