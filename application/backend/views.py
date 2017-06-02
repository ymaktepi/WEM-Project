#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from flask import Flask, render_template, redirect, url_for, request, jsonify

from backend import app, indexer

from wem.index.quouairiManadgeure import QueryManager

listFields = ['tags',
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

@app.route("/api/search/<int:page>", methods=["GET"])
def search(page):
    results = []
    words = request.args.get('query')
    if words is not None:
        words = str(request.args.get('query'))

    scoring = request.args.get('scoring')
    if scoring is not None:
        scoring = str(request.args.get('scoring'))


    metadata = {
        'category': request.args.getlist('category'),
        'language': request.args.getlist('language'),
        'tool': request.args.getlist('tool'),
        'tags': request.args.getlist('tags'),
    }

    try:
        with QueryManager(indexer.getIndex(), listFields) as qm:
            res = qm.text_query(scoring, words, metadata, page)

            found = res.scored_length()
            on = len(res)

            for result in res:
                results.append({field: result[field] for field in listFields})
                results[-1]['score'] = result.score
                results[-1]['url'] = result['url']

        return jsonify({
            'metadata': {
                'found': found,
                'on': on,
                'hasMore': found < on
            },
            'data': results
        })
    except Exception:
        return jsonify({'message': 'No input provided!'}), 426

@app.route("/api/terms/<field>", methods=["GET"])
def categories(field):
    searcher = indexer.getIndex().searcher()
    try:
        res = [cat.decode("utf-8") for cat in list(searcher.lexicon(field))]
        return jsonify(res)
    except Exception:
        return jsonify({'message': 'This field doesnt exists!'}), 426
