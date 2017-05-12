#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for

from wem import app

@app.route("/")
def route_home():
    return "okay"
