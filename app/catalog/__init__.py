## catalog package folder
from flask import Blueprint

## where to look for templates file
main = Blueprint("main",__name__,template_folder ="templates")

from app.catalog import routes