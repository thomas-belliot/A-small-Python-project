This project aims to develop a Python application that reads a given picture at low resolution and generates a scalable version (as a .svg file) that can be used as a high-resolution wallpaper on any computer.
The application reads an input file (file.png) and produces an output file (file.svg) that can be opened and rendered with any compatible application.

The functions in the src/ folder have been developed using [this website](https://www.redblobgames.com/grids/hexagons/) and the document "Notes.pdf" inside the img/ folder. This latter were used to find the correct formulae.


Tests to pass before every commit:
uv run ruff format .
uv run ruff check .
uv run mypy src
uv run pytest --cov=src --cov-report=term-missing