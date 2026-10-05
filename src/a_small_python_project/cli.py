"""Command-line interface for fizzbuzz_kata."""

import argparse

from a_small_python_project.png2svg import convert


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="convert-kata",
        description="Convert a given value into a svg file",
    )
    parser.add_argument(
        "src_path", type=str, nargs="?", help="The file where to retrieve the image from"
    )
    parser.add_argument("--save_path", type=str, help="Where store the svg file.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.src_path is not None and args.save_path is not None:
        convert(args.src_path, args.save_path)
        print(f"Look at {args.save_path} for the output")
    elif args.src_path is not None:
        convert(args.src_path, "output_image.svg")
        print("Look at output_image.svg for the output")

    else:
        parser.error("You should provide at least the location of the image")


if __name__ == "main":
    main()
