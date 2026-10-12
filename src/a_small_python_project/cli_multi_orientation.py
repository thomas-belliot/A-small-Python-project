"""Command-line interface for the python project."""

import argparse

from a_small_python_project.png2svg_multi_orientation import convert_multi as convert_multi


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="convert-kata",
        description="Convert a given value into a svg file",
    )
    parser.add_argument(
        "src_path", type=str, nargs="?", help="The file where to retrieve the image from"
    )
    parser.add_argument("--save_path", type=str, help="Where store the svg file.")
    parser.add_argument(
        "--orientation", type=str, help="What is the orientation chosen ('flat' or 'pointy')"
    )
    parser.add_argument("--size", type=int, help="Choose the size of the hexagons")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if (
        args.src_path is not None
        and args.save_path is not None
        and args.orientation is not None
        and args.size is not None
    ):
        assert args.size > 0
        convert_multi(
            input_filename=args.src_path,
            output_filename=args.save_path,
            size=args.size,
            orientation=args.orientation,
        )
        print(f"Look at {args.save_path} for the output")

    elif args.src_path is not None and args.orientation is not None and args.size is not None:
        assert args.size > 0
        convert_multi(
            input_filename=args.src_path,
            output_filename="output_image.svg",
            size=args.size,
            orientation=args.orientation,
        )
        print(f"Look at {args.save_path} for the output")

    elif args.src_path is not None and args.orientation is not None:
        convert_multi(
            input_filename=args.src_path,
            output_filename="output_image.svg",
            orientation=args.orientation,
        )
        print("Look at output_image.svg for the output")

    elif args.src_path is not None:
        convert_multi(input_filename=args.src_path, output_filename="output_image.svg")
        print("Look at output_image.svg for the output")

    else:
        parser.error("You should provide at least the location of the image")


if __name__ == "main":
    main()
