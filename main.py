from flask import Flask, request, abort
import os
import sys
app = Flask(__name__)

app_dir = os.path.abspath(os.path.dirname(__file__))
print(app_dir)
sys.path.insert(0, app_dir)

import controllers
