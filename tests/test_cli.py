from a_small_python_project.cli import build_parser
from a_small_python_project.png2svg import load_image


def test_parser_accepts_single_input():
    args = build_parser().parse_args(["img/image.jpg"])
    assert args.src_path == "img/image.jpg"
    assert load_image("img/image.jpg").size == (900, 506)


def test_parser_accepts_two_inputs():
    args = build_parser().parse_args(["img/image.jpg", "--save_path=output_image.svg"])
    assert args.src_path == "img/image.jpg"
    assert args.save_path == "output_image.svg"
    assert load_image("img/image.jpg").size == (900, 506)
