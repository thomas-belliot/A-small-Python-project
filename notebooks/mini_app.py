import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from math import cos, pi, sin, sqrt

    import marimo as mo
    from PIL import Image

    return Image, cos, mo, pi, sin, sqrt


@app.cell
def _():
    # Load the image
    # image = Image.open("../img/image.jpg")
    return


@app.cell
def _(Image):
    def load_image(filename: str) -> Image.Image:
        """Load an image"""
        return Image.open(filename)

    image = load_image("img/image.jpg")
    assert image.size == (900, 506)
    assert image.mode == "RGB"
    assert image.getpixel((0, 0)) == (22, 199, 232)
    # image
    return image, load_image


@app.cell
def _(image):
    print(image.size, image.mode)

    print(image.getpixel((0, 0)))
    px = image.load()
    print(px[0, 0])


@app.cell
def _(sqrt):
    # I choose the pointy top orientation
    def hexagon_center(row: int, column: int, size: float) -> tuple[float, float]:
        """Given a row, a column and the radius (size), return the center of the hexagon for this location and size"""
        x = (
            sqrt(3) * size * (column + 1 / 2 + 1 / 2 * (row % 2))
        )  # The vertical distance is vert = sqrt(3) * size
        y = (
            size * (1 + 3 / 2 * row)
        )  # the horizontal distance between adjacent hexagon centers is horiz = 3/2 * size
        return x, y

    assert hexagon_center(0, 0, 20) == (20 * sqrt(3) / 2, 20)
    assert hexagon_center(0, 1, 20) == (20 * sqrt(3) * (1 / 2 + 1), 20)
    assert hexagon_center(1, 0, 20) == (20 * sqrt(3), 20 * (1 + 3 / 2))
    assert hexagon_center(10, 5, 20) == (
        20 * sqrt(3) * (5 + 1 / 2 + 1 / 2 * (10 % 2)),
        20 * (1 + 10 * 3 / 2),
    )


@app.cell
def _(cos, pi, sin):
    # Taken from https://www.redblobgames.com/grids/hexagons/, "Angles" section
    def hexagon_points(cx: float, cy: float, size: float) -> list[tuple[float, float]]:
        """Calculate the extremitiy points of an hexagon, given the center of this hexagon.
        Order of the points : start at the bottom right (pointy top orientation), and turns by the left"""
        hexa_extremity = []
        for i in range(6):
            angle_deg = 60 * i - 30  # °
            angle_rad = pi / 180 * angle_deg
            hexa_extremity.append(
                (cx + size * cos(angle_rad), cy + size * sin(angle_rad))
            )
        return hexa_extremity

    test = hexagon_points(4.96, 8.68, 10)
    test = [
        (round(test[k][0], 1), round(test[k][1], 1)) for k in range(len(test))
    ]  # I did not succeed to put the points exactly at the right place on Geogebra
    assert (13.6, 13.7) in test
    assert (13.6, 3.7) in test
    assert (14, 4) not in test
    assert len(test) == 6
    return (hexagon_points,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A = (xA, yA), B = (xB, yB), P = (x, y) (pixel) are organized this way
        A
    P -----
        B
    (yA > y) != (yB > y) → Check if A and B are on both side of the line starting from P
    We should have  yA > y → False and yB > y → True

    And (xB - xA) * (y - yA) / (yB - yA) + xA calculates the coordinate X of the point where the side of the hexagon meets the horizontal line y (we check if the intersection is to the right of the point), i.e. this value must be positive if P is on the left compare to [A,B].

    The full method is explained [here](https://www.geeksforgeeks.org/c/point-in-polygon-in-c/#method-1-using-ray-casting-algorithm)
    """)


@app.cell
def _(hexagon_points):
    def ray_intersects_edge(
        x: float, y: float, xi: float, yi: float, xj: float, yj: float
    ) -> bool:

        # Does the segment cross the height of the point?
        crosses_y = (yi > y) != (yj > y)

        if not crosses_y:
            return False

        # Where does the segment meet the horizontal line there?
        x_intersection = (xj - xi) * (y - yi) / (yj - yi) + xi

        # Is the intersection to the right of the point?
        return x < x_intersection

    def is_point_in_hexagon(
        x: float, y: float, cx: float, cy: float, size: float
    ) -> bool:
        """Decide whether the point x, y is inside the hexagon defined by its center (cx, cy) and its size
        Formula based on the Ray Casting method
        The method consists of mentally drawing a horizontal half-right from the point to the right and counting the number of sides of
        the polygon that it passes through. Odd number → interior ; even number → outside.
        """

        hexa_extremity = hexagon_points(cx, cy, size)

        inside = False
        j = len(hexa_extremity) - 1

        for i in range(len(hexa_extremity)):
            xi, yi = hexa_extremity[i]
            xj, yj = hexa_extremity[j]

            if ray_intersects_edge(
                x,
                y,
                xi,
                yi,
                xj,
                yj,
            ):
                inside = not inside
                # number of even crossings → False
                # number of odd crossings → True
            j = i

        return inside

    x_False = [-4, -2, 0, 8, 0, 14, 10]
    y_False = [4, 2, 16, 0, 0, 10, 16]
    x_True = [2, -2, 2, 3, 6, 13, 8]
    y_True = [2, 14, 16, 16, 0, 10, 8]

    for k in range(len(x_False)):
        assert is_point_in_hexagon(x_True[k], y_True[k], 4.96, 8.68, 10) == True
        assert is_point_in_hexagon(x_False[k], y_False[k], 4.96, 8.68, 10) == False
    return (is_point_in_hexagon,)


"""@app.cell
def _(image):
    image.size"""


@app.cell
def _(Image, image, is_point_in_hexagon, sqrt):
    def sample_color(
        image: Image.Image,
        cx: float,
        cy: float,
        size: float,
    ) -> tuple[int, int, int]:
        """Sample the color for the hexagon with center at position (cx, cy)"""
        pixels: list[tuple[int, int, int]] = []

        min_x = max(0, int(cx - sqrt(3) * size / 2))
        max_x = min(image.width - 1, int(cx + sqrt(3) * size / 2))

        min_y = max(0, int(cy - size))
        max_y = min(image.height - 1, int(cy + size))

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if is_point_in_hexagon(x, y, cx, cy, size):
                    pixels.append(image.getpixel((x, y)))

        if len(pixels) == 0:  # If there is not a single point in the hexagon
            return (0, 0, 0)

        red = sum(pixel[0] for pixel in pixels) // len(pixels)
        green = sum(pixel[1] for pixel in pixels) // len(pixels)
        blue = sum(pixel[2] for pixel in pixels) // len(pixels)

        return red, green, blue

    # It will be hard to test, but we can at least test that we got (0,0,0) outside the image
    assert sample_color(image, 900, -10, 10) == (0, 0, 0)
    assert sample_color(image, 2000, 1000, 10) == (0, 0, 0)
    assert sample_color(image, 910, 200, 10) == (0, 0, 0)
    assert sample_color(image, 300, 525, 10) == (0, 0, 0)
    return (sample_color,)


@app.cell
def _():
    def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        """Just a conversion from rgb to hexadecimal"""
        red, green, blue = rgb
        return f"#{red:02x}{green:02x}{blue:02x}"

    assert rgb_to_hex((0, 0, 0)) == "#000000"
    assert rgb_to_hex((10, 0, 12)).upper() == "#0A000C"
    assert rgb_to_hex((124, 52, 12)).upper() == "#7C340C"
    assert rgb_to_hex((124, 50, 12)).upper() == "#7C320C"
    return (rgb_to_hex,)


@app.cell
def _(hexagon_points, rgb_to_hex):
    def generate_hexagon(
        cx: float, cy: float, size: float, rgb: tuple[int, int, int]
    ) -> str:
        """Create an hexagon by returning the extremity of the hexagon, and it's color with svg format
        ex of output : <polygon points="17.32,10.00 0.00,20.00 -17.32,10.00 -17.32,-10.00 0.00,-20.00 17.32,-10.00" fill="#7f543f" />
        """
        points = hexagon_points(cx, cy, size)

        points_string = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)

        color = rgb_to_hex(rgb)

        return f'<polygon points="{points_string}" fill="{color}" />'

    return (generate_hexagon,)


@app.cell
def _(Image, generate_hexagon, sample_color, sqrt):
    def generate_svg(image: Image.Image, size: float) -> str:
        """Generate the content of the svg file for the given image"""

        width, height = image.size

        polygons = []
        row = 0

        while True:
            cy = size * (1 + 1.5 * row)
            if cy >= height + size:  # Out of the image
                break

            column = 0

            while True:
                cx = sqrt(3) * size * (column + 0.5 + 0.5 * (row % 2))

                if cx >= width + size:  # Out of the image
                    break

                rgb = sample_color(
                    image,
                    cx,
                    cy,
                    size,
                )
                polygon = generate_hexagon(cx, cy, size, rgb)
                polygons.append(polygon)
                column += 1
            row += 1

        return "\n".join(
            [
                (
                    f'<svg xmlns="http://www.w3.org/2000/svg" '
                    f'width="{width}" height="{height}" '
                    f'viewBox="0 0 {width} {height}">'
                ),
                *polygons,
                "</svg>",
            ]
        )

    return (generate_svg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)


@app.cell
def _(generate_svg, load_image):
    def convert(
        input_filename: str, output_filename: str, hex_size: float = 20
    ) -> None:
        """This functions open an image at location 'input_filename', and convert it into svg file"""
        image = load_image(input_filename)

        svg_content = generate_svg(image, hex_size)

        with open(output_filename, "w") as f:
            f.write(svg_content)

    return (convert,)


@app.cell
def _(convert):
    convert("img/image.jpg", "img/test3.svg")


if __name__ == "__main__":
    app.run()
