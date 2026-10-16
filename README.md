# A Small Python Project

This project aims to develop a Python application that reads a given picture at low resolution and generates a scalable version (as a .svg file) that can be used as a high-resolution wallpaper on any computer.
The application reads an input file (img/image.jpg) and produces an output svg file that can be opened and rendered with any compatible application.

The functions in the `src/` folder have been developed using [this website](https://www.redblobgames.com/grids/hexagons/) and the document `img/Notes.pdf`. The latter was used to find the correct formulas. In addition, two versions have been developed: one version with the "pointy-top" orientation (everything related to "png2svg"), and later a version with "flat-top" orientation (everything related to "png2svg_multi_orientation"). The second version is more complete as it is a combination of both approaches, allowing a user to choose both the size and the orientation of the hexagons.  


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
*Example of use* : `uv run convert_multi-kata img/image.jpg --save_path="img/test.svg" --orientation="pointy" --size=30`

### *How to run the website locally :*  
uv run marimo check notebooks/transform_explorer.py --select MW  
uv sync --locked --all-groups  
uv build  
cp dist/a_small_python_project-*.whl notebooks/public/  
uv run marimo export html-wasm notebooks/transform_explorer.py -o site --mode run  
uv run python -m http.server -d site  


### *Organization of the project*
.  
├── -cov-report=term-missing  
├── -cov=src  
├── dist  
│   ├── a_small_python_project-0.1.0-py3-none-any.whl  
│   └── a_small_python_project-0.1.0.tar.gz  
├── img {This directory contains some explanations about how }  
│   ├── Hexagon_test.png  
│   ├── image.jpg  
│   └── Notes.pdf  
├── notebooks  
│   ├── __marimo__  
│   ├── mini_app.py **{Draft notebook to try the functions; not really documented.}**  
│   ├── public  
│   │   ├── a_small_python_project-0.1.0-py3-none-any.whl  
│   │   └── img  
│   │       └── image.jpg  
│   └── transform_explorer.py **{Use what has been done in the src directory to create an interactive webpage.}**  
├── pyproject.toml  
├── README.md  
├── src  
│   └── a_small_python_project  
│       ├── cli_multi_orientation.py **{File to create the command-line interface, allowing you to choose the size and orientation}**  
│       ├── cli.py **{File to create the command-line interface, only for "pointy-top" orientation and size=20}**  
│       ├── __init__.py  
│       ├── png2svg_multi_orientation.py **{File with functions allowing choices of orientation and size}**  
│       ├── png2svg.py **{File with functions only for "pointy-top" orientation and size=20}**  
├── tests **{Tests of files whose name is what follows "test_"}**  
│   ├── test_cli_multi_orientation.py  
│   ├── test_cli.py  
│   ├── test_png2svg_multi_orientation.py  
│   └── test_png2svg.py  
└── uv.lock  

### *A small remark*
The threshold for the test which must be passed with mypy has been set to 40% because there are some functions which are quite hard to test.