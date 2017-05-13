#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, jsonify

from backend import app, indexer

from wem.index.quouairiManadgeure import QueryManager

listFields = ['text',
              'tags',
              'title',
              'tag_title',
              'meta_title',
              'meta_description',
              'meta_keywords',
              'meta_og_title',
              'meta_og_description',
              'meta_twitter_title',
              'meta_twitter_description']


@app.route("/")
def route_home():
    return render_template("index.html")


@app.route("/api/search", methods=["GET"])
def search():
    results = []
    words = str(request.args.get('query'))
    with QueryManager(indexer.getIndex(), listFields) as qm:
        for result in qm.textQuouairiz(words):
            results.append({field: result[field] for field in listFields})
            results[-1]['score'] = result.score
            results[-1]['url'] = result['url']

    return jsonify(results)
