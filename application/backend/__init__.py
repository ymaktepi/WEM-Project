# -*- coding: utf-8 -*-

from flask import Flask
from backend.loadScraper import loadScraper

app = Flask(__name__)
indexer, toolIndex = loadScraper()

import backend.views
import backend.errors