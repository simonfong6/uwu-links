#!/usr/bin/env python3
"""
Server code to track number of visitors.
"""
import logging
import json
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import render_template
from flask import url_for


app = Flask(__name__)


class Links(dict):
    pass


links = Links()


@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/go/<short_link>')
def go(short_link):
    global links
    if short_link not in links:
        print(links)
        return redirect(url_for('add', short_link=short_link))
    else:
        return redirect(links[short_link])

@app.route('/add/<short_link>', methods=['GET', 'POST'])
def add(short_link):
    global links
    if request.method == 'GET':
        return render_template('add.jinja', short_link=short_link)
    elif request.method == 'POST':
        url = request.form['url']
        links[short_link] = url
        print("Adding {}".format(url))
        return redirect(url_for('go', short_link=short_link))



def main(args):

    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=args.port)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p', '--port',
                        help="Port that the server will run on.",
                        type=int,
                        default=3333)
    parser.add_argument('-d', '--debug',
                        help="Whether or not to run in debug mode.",
                        default=False,
                        action='store_true')
    parser.add_argument('--prod',
                        help="Whether or not to run in prod mode.",
                        default=False,
                        action='store_true')

    parser.add_argument('--no_log',
                        help="Whether to not keep logs.",
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    main(args)