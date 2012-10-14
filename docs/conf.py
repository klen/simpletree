# -*- coding: utf-8 -*-
import os
import sys

from simpletree import __version__ as release

project = 'SimpleTree'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
copyright = u'2012, Kirill Klenov'
version = '.'.join(release.split('.')[:2])
exclude_patterns = ['_build']
html_use_modindex = False
html_show_sphinx = False
htmlhelp_basename = '{0}doc'.format(project)
latex_documents = [
    ('index', '{0}.tex'.format(project), u'{0} Documentation'.format(project),
        u'Kirill Klenov', 'manual'),
]
latex_use_modindex = False
latex_elements = {
    'fontpkg':      r'\usepackage{mathpazo}',
    'papersize':    'a4paper',
    'pointsize':    '12pt',
    'preamble':     r'\usepackage{flaskstyle}'
}
latex_use_parts = True
latex_additional_files = ['flaskstyle.sty', 'logo.pdf']
man_pages = [
    ('index', project.lower(), u'{0} Documentation'.format(project),
     [u'Kirill Klenov'], 1)
]
pygments_style = 'tango'
html_theme = 'default'
html_theme_options = {}
