# A Small Python Project

This project aims to develop a Python application that reads a given picture at low resolution and generates a scalable version (as a .svg file) that can be used as a high-resolution wallpaper on any computer.
The application reads an input file (file.png) and produces an output file (file.svg) that can be opened and rendered with any compatible application.

The functions in the `src/` folder have been developed using [this website](https://www.redblobgames.com/grids/hexagons/) and the document `Notes.pdf` inside the `img/` folder. This latter were used to find the correct formulae.


### *Tests to pass before every commit:*  
uv run ruff format .  
uv run ruff check .  
uv run mypy src  
uv run pytest --cov=src --cov-report=term-missing  

### *How to convert an image from the command line interface :*  
uv run convert-kata [image_path] [--output_path]  
/!\ Do not forget to add the '.svg' at the end of the output_path  

### *How to run the website locally :*  
uv run marimo check notebooks/transform_explorer.py --select MW  
uv sync --locked --all-groups  
uv build  
uv run marimo export html-wasm notebooks/transform_explorer.py -o site --mode run  
uv run python -m http.server -d site  