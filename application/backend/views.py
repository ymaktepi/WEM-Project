#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, jsonify

from backend import app, indexer

from wem.index.quouairiManadgeure import QueryManager

listFields = ['text',
              'tags',
              'title',
              'tag_title',
              'tool',
              'language',
              'category',
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
    filters = str(request.args.get('filters'))
    # TODO integrate the filters in the request
    with QueryManager(indexer.getIndex(), listFields) as qm:
        for result in qm.textQuouairiz(words):
            results.append({field: result[field] for field in listFields})
            results[-1]['score'] = result.score
            results[-1]['url'] = result['url']

    return jsonify(results)

@app.route("/api/terms/<field>", methods=["GET"])
def categories(field):
    searcher = indexer.getIndex().searcher()
    try:
        res = [cat.decode("utf-8") for cat in list(searcher.lexicon(field))]
        return jsonify(res)
    except Exception:
        return jsonify({'message': 'this field doesnt exists'}), 426
