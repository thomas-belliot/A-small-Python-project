import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from a_small_python_project.png2svg import convert, load_image

    mo.md(
        r"""
        # png2svg Explorer
        Select the path to your image below and see the result
       """
    )
    return convert, load_image, mo


@app.cell
def _():
    """src_path = mo.ui.text_area(placeholder="Enter the path to the image you want to process")
    src_path"""
    return


@app.cell
def _():
    """save_path = mo.ui.text_area(placeholder="Enter the path where to store your processed image.
    !!! Add the .svg atthe end !!!")
    save_path"""
    return


@app.cell
def _(load_image):
    src_path = "img/image.jpg"
    save_path = "img/image2.svg"
    img = load_image(src_path)  # src_path.value
    return img, save_path, src_path


@app.cell
def _():
    print("Here is your image")
    return


@app.cell
def _(img):
    img
    return


@app.cell
def _(mo):
    size_hexagon = mo.ui.slider(1, 200, value=20, label="Size of the hexagon")
    size_hexagon
    return (size_hexagon,)


@app.cell
def _(convert, save_path, size_hexagon, src_path):
    convert(src_path, save_path, size_hexagon.value)  # save_image.value,
    print("Image processed")
    return


@app.cell
def _(mo, save_path):
    mo.image(src=save_path)
    return


if __name__ == "__main__":
    app.run()
