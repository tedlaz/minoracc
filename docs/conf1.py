#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.dirname(__file__))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode']

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'minoracc'
copyright = '2019, Ted Lazaros'
author = 'Ted Lazaros'
version = '1.0.1'
release = '1.0.1'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
intersphinx_mapping = {
    'python': ('http://python.readthedocs.io/en/latest/', None),
    'sphinx': ('http://sphinx.readthedocs.io/en/latest/', None),
}
todo_include_todos = True
html_theme = 'default'
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}
htmlhelp_basename = 'minoraccdoc'
latex_elements = {}
latex_documents = [
    (master_doc, 'minoracc.tex', 'minoracc Documentation',
     'Ted Lazaros', 'manual'),
]
man_pages = [
    (master_doc, 'minoracc', 'minoracc Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'minoracc', 'minoracc Documentation',
     author, 'minoracc', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
