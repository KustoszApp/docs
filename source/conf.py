# Configuration file for the Sphinx documentation builder.
#
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = 'Kustosz'
copyright = '2022, Mirek Długosz'
author = 'Mirek Długosz'
extensions = [
    "myst_parser",
    "sphinx_design"
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'furo'
html_static_path = ['_static']

myst_enable_extensions = [
    "colon_fence",
]
myst_heading_anchors = 3
