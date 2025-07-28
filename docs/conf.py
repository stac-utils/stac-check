# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Options for including images from README ----------------------------------
import os
import shutil

project = "stac-check"
copyright = "2025, Jonathan Healy"
author = "Jonathan Healy"
release = "1.7.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_click",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = []

# Create _static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "_static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Copy assets from project root to _static directory
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
if os.path.exists(assets_dir):
    for file in os.listdir(assets_dir):
        src = os.path.join(assets_dir, file)
        dst = os.path.join(static_dir, file)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

# Now that we've copied files, update static path
html_static_path = ["_static"]

myst_heading_anchors = 3  # Generate anchors for h1, h2, and h3

# Configure myst-parser to handle images
myst_url_schemes = ("http", "https", "mailto", "ftp")

html_css_files = [
    "custom.css",
]
