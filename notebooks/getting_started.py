import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from samvad.utils.data import get_data
    return (get_data,)


@app.cell
def _(get_data):
    get_data()
    return


if __name__ == "__main__":
    app.run()
