from __future__ import annotations

import os
import sys

ROOT = os.path.abspath('..')
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

project = 'PyMUMPS'
author = 'PyMUMPS contributors'

try:
    from mumps import __version__ as version
except (ImportError, AttributeError):
    version = 'unknown'
release = version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_copybutton',
]

autosummary_generate = True
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autoclass_content = 'both'

autodoc_mock_imports = [
    'mpi4py',
]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

myst_enable_extensions = [
    'colon_fence',
    'deflist',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_title = f'{project} {release}'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy', None),
}
