#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request

from backend import app, indexer

from wem.index.quouairiManadgeure import QueryManager


@app.route("/")
def route_home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():

    results = []
    words = str(request.args.get('query'))
    with QueryManager(indexer.getIndex(), 'text') as qm:
        for result in qm.textQuouairiz(words):
            results.append(str(result['url']))

    return str(results)

