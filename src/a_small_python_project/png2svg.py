from math import cos, pi, sin, sqrt

from PIL import Image


def load_image(filename: str) -> Image.Image:
    """Load the image located at "filename"

    Args:
        filename (str): localisation of the image

    Returns:
        Image.Image: Image object containing information about the image
    """
    return Image.open(filename)


def hexagon_center(row: int, column: int, size: float) -> tuple[float, float]:
    """Given a row, a column and the size of the hexagon (size), return the center of the hexagon for this location and size
    Look at the 'Notes.pdf' file in the 'img' folder tounderstand the formula. I chose the pointy top orientation.
    Returns:
        tuple[float, float]: Center of the hexagon at a given (row, column)
    """
    x = (
        sqrt(3) * size * (column + 1 / 2 + 1 / 2 * (row % 2))
    )  # The vertical distance is vert = sqrt(3) * size
    y = size * (
        1 + 3 / 2 * row
    )  # the horizontal distance between adjacent hexagon centers is horiz = 3/2 * size
    return x, y


def hexagon_points(cx: float, cy: float, size: float) -> list[tuple[float, float]]:
    """Calculate the extremitiy points of an hexagon, given the center of this hexagon and its size.
    Order of the points : start at the bottom right (pointy top orientation), and turns by the left
    Taken from https://www.redblobgames.com/grids/hexagons/, "Angles" section. I chose the pointy top orientation.

    Returns:
        list[tuple[float, float]]: The six points which represent the extremity of the hexagon
    """
    hexa_extremity = []
    for i in range(6):
        angle_deg = 60 * i - 30  # °
        angle_rad = pi / 180 * angle_deg
        hexa_extremity.append((cx + size * cos(angle_rad), cy + size * sin(angle_rad)))
    return hexa_extremity


def ray_intersects_edge(
    x: float, y: float, xi: float, yi: float, xj: float, yj: float
) -> bool:
    """Intermediate function to calulate whether a point P(x,y) is between two points I(xi, yi) and J(j, yj).
    Look at the notebook "mini_app.py" for more details

    Args:
        x (float): x coordinate of P
        y (float): y coordinate of P
        xi (float): x coordinate of I
        yi (float): y coordinate of I
        xj (float): x coordinate of J
        yj (float): y coordinate of J

    Returns:
        bool: whether the point is well-located to be inside the hexagon
    """
    # Does the segment cross the height of the point?
    crosses_y = (yi > y) != (yj > y)
    if not crosses_y:
        return False
    # Where does the segment meet the horizontal line there?
    x_intersection = (xj - xi) * (y - yi) / (yj - yi) + xi
    # Is the intersection to the right of the point?
    return x < x_intersection


def is_point_in_hexagon(x: float, y: float, cx: float, cy: float, size: float) -> bool:
    """Decide whether the point (x, y) is inside the hexagon defined by its center (cx, cy) and its size
    Formula based on the Ray Casting method
    The method consists of mentally drawing a horizontal half-right from the point to the right and counting the number of sides of
    the polygon that it passes through. Odd number → interior ; even number → outside.

    Args:
        x (float): x coordinate of the point to consider
        y (float): y coordinate of the point to consider
        cx (float): x value for the center of the hexagon
        cy (float): y value for the center of the hexagon
        size (float): size of the hexagon as defined here : https://www.redblobgames.com/grids/hexagons/ (pointy top orientation)

    Returns:
        bool: if the point is inside the hexagon or not
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


def sample_color(
    image: Image.Image,
    cx: float,
    cy: float,
    size: float,
) -> tuple[int, int, int]:
    """Sample the color for the hexagon with center at position (cx, cy) and with a given size

    Args:
        image (Image.Image): image where we consider the pixels
        cx (float): x value for the center of the hexagon
        cy (float): y value for the center of the hexagon
        size (float): size of the hexagon as defined here : https://www.redblobgames.com/grids/hexagons/ (pointy top orientation)

    Returns:
        tuple[int, int, int]: RGB values which average the color of the pixels inside the hexagon in the image
    """

    pixels = []

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

    red = 0
    green = 0
    blue = 0

    for pixel in pixels:
        if isinstance(pixel, tuple):
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]
    red = red // len(pixels)
    green = green // len(pixels)
    blue = blue // len(pixels)

    return red, green, blue


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Just a conversion from rgb to hexadecimal

    Args:
        rgb (tuple[int, int, int]): Tuple representing a color in RGB

    Returns:
        str: The same color with the hexadecimal representation
    """
    red, green, blue = rgb
    return f"#{red:02x}{green:02x}{blue:02x}"


def generate_hexagon(
    cx: float, cy: float, size: float, rgb: tuple[int, int, int]
) -> str:
    """Create an hexagon by returning the extremity of the hexagon, and it's color according to svg format

    Args:
        cx (float): x value for the center of the hexagon
        cy (float): y value for the center of the hexagon
        size (float): size of the hexagon as defined here : https://www.redblobgames.com/grids/hexagons/ (pointy top orientation)
        rgb (tuple[int, int, int]): The RGB value for this hexagon

    Returns:
        str: svg format description of the hexagon
        ex of output : <polygon points="17.32,10.00 0.00,20.00 -17.32,10.00 -17.32,-10.00 0.00,-20.00 17.32,-10.00" fill="#7f543f" />
    """
    points = hexagon_points(cx, cy, size)

    points_string = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)

    color = rgb_to_hex(rgb)

    return f'<polygon points="{points_string}" fill="{color}" />'


def generate_svg(image: Image.Image, size: float) -> str:
    """Generate the content of the svg file for the given image

    Args:
        image (Image.Image): The image to transform into svg
        size (float): the size chosen for each hexagon

    Returns:
        str: The svg format description of the image represented thanks to hexagonal grid
    """
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


def convert(input_filename: str, output_filename: str, size: float = 20) -> None:
    """Open an image at location 'input_filename', convert it into svg file, and save the result at location 'output_filename'

    Args:
        input_filename (str): Location of the image to transform
        output_filename (str): Location for the new image with svg format
        size (float, optional): size chosen for each hexagon. Defaults to 20.
    """
    image = load_image(input_filename)

    svg_content = generate_svg(image, size)

    with open(output_filename, "w") as f:
        f.write(svg_content)
