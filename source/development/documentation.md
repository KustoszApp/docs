# Documentation

Documentation, available at [docs.kustosz.org](https://docs.kustosz.org/), is written in [MyST](https://myst-parser.readthedocs.io/en/latest/sphinx/intro.html), which is [CommonMark](https://commonmark.org/) with support for [Sphinx](https://www.sphinx-doc.org) directives. Basically, it's Markdown.

Documentation is built using Sphinx, which is Python package. It requires any Python 3 version supported by Sphinx.

## Preparing development environment

Clone Github repo:

    git clone https://github.com/KustoszApp/docs

Create new virtual environment:

    python3 -m venv path/to/virtualenv

Activate virtual environment:

    source path/to/virtualenv/bin/activate

Install dependencies:

    pip install -r requirements.txt

## Running current development version

Run server:

    python3 run_livereload.py

Kustosz documentation will be available at <http://127.0.0.1:5500/>. Website refreshes automatically as you change documentation source files.
