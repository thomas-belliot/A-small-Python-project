# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.25.1",
#     "pillow>=12.3.0",
# ]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        r"""
        # png2svg Explorer
        See an example of the transformer
       """
    )
    return (mo,)


@app.cell
def _():
    from io import BytesIO
    from urllib.request import urlopen

    from PIL import Image

    def load_image_from_url(url: str) -> Image.Image:
        with urlopen(url) as response:
            image_data = response.read()

        return Image.open(BytesIO(image_data))

    return (load_image_from_url,)


@app.cell
def _(mo):
    public_dir = mo.notebook_location() / "public"

    src_path = str(public_dir / "img" / "image.jpg")
    return (src_path,)


@app.cell
def _():
    """Here is the original image"""
    return


@app.cell
def _(load_image_from_url, src_path):
    img = load_image_from_url(src_path)
    return (img,)


@app.cell
def _(img):
    img
    return


@app.cell
def _(mo):
    size_hexagon = mo.ui.slider(1, 50, value=20, label="Size of the hexagon")
    size_hexagon
    return (size_hexagon,)


@app.cell
def _(mo):
    # https://docs.marimo.io/api/inputs/multiselect/#marimo.ui.multiselect
    orientation_hexa = mo.ui.multiselect(
        options=["Flat-top", "Pointy-top"], label="Which orientation do you want ?"
    )
    orientation_hexa
    return (orientation_hexa,)


@app.cell
def _():
    """Here is the converted image with hexagons"""
    return


@app.cell
def _(img, orientation_hexa, size_hexagon):
    from a_small_python_project.png2svg_multi_orientation import generate_svg_multi

    orientation = "flat"
    if orientation_hexa.value != [] and orientation_hexa.value[0] == "Pointy-top":
        orientation = "pointy"

    svg_content = generate_svg_multi(img, size_hexagon.value, orientation)
    return (svg_content,)


@app.cell
def _(mo, svg_content):
    mo.Html(svg_content)
    return


if __name__ == "__main__":
    app.run()
