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
This first command will use the **pointy top orientation**, with a **size of 20** :  
uv run convert-kata [image_path] [--save_path]  

This command is more general and allows to choose between "pointy" or "flat" orientation, and the size of your choice :  
uv run convert_multi-kata [image_path] [--save_path] [--orientation] [--size]  

/!\ Do not forget to **add the '.svg' at the end of the save_path**  
*Example of use* : `uv run convert_multi-kata img/image.jpg --save_path="img/test3.svg" --orientation="pointy" --size=30`

### *How to run the website locally :*  
uv run marimo check notebooks/transform_explorer.py --select MW  
uv sync --locked --all-groups  
uv build  
cp dist/a_small_python_project-*.whl notebooks/public/  
uv run marimo export html-wasm notebooks/transform_explorer.py -o site --mode run  
uv run python -m http.server -d site  