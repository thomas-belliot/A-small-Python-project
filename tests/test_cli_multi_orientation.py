from a_small_python_project.cli_multi_orientation import build_parser
from a_small_python_project.png2svg_multi_orientation import load_image


def test_parser_accepts_single_input():
    args = build_parser().parse_args(
        [
            "img/image.jpg",
        ]
    )
    assert args.src_path == "img/image.jpg"
    assert load_image("img/image.jpg").size == (900, 506)


def test_parser_accepts_several_input():
    args = build_parser().parse_args(["img/image.jpg", "--orientation=flat"])
    assert args.src_path == "img/image.jpg"
    assert args.orientation == "flat"
    assert load_image("img/image.jpg").size == (900, 506)


def test_parser_accepts_several_input2():
    args = build_parser().parse_args(["img/image.jpg", "--orientation=flat", "--size=26"])
    assert args.src_path == "img/image.jpg"
    assert args.orientation == "flat"
    assert args.size == 26
    assert load_image("img/image.jpg").size == (900, 506)


def test_parser_accepts_two_inputs():
    args = build_parser().parse_args(["img/image.jpg", "--save_path=output_image.svg"])
    assert args.src_path == "img/image.jpg"
    assert args.save_path == "output_image.svg"
    assert load_image("img/image.jpg").size == (900, 506)
