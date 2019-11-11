#!/usr/bin/env python3
"""
Server code to track number of visitors.
"""
import logging

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import redirect
from flask import render_template
from flask import url_for

from links import Links


app = Flask(__name__)


links = None


@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/go/<short_link>')
def go(short_link):
    global links
    if not links.has(short_link):
        return redirect(url_for('add', short_link=short_link))
    else:
        url = links.get(short_link)
        print("Redirecting '{short_link}' -> '{url}'.".format(
            short_link=short_link,
            url=url
        ))
        return redirect(url)

@app.route('/add/<short_link>', methods=['GET', 'POST'])
def add(short_link):
    global links
    if request.method == 'GET':
        return render_template('add.jinja', short_link=short_link)
    elif request.method == 'POST':
        url = request.form['url']

        links.insert(short_link, url)
        print("Adding '{short_link}' -> '{url}'.".format(
            short_link=short_link,
            url=url
        ))

        return redirect(url_for('add_after', short_link=short_link))

@app.route('/add-after/<short_link>')
def add_after(short_link):
    global links
    if not links.has(short_link):
        return redirect(url_for('add', short_link=short_link))
    else:
        url = links.get(short_link)
        print("Redirecting '{short_link}' -> '{url}'.".format(
            short_link=short_link,
            url=url
        ))
        return render_template(
            'add_after.jinja',
            short_link=short_link,
            url=url)

@app.route('/directory')
def directory():
    global links
    context = {
        'short_link': 'shorties',
        'url': 'urlies'
    }
    link_dicts = links.get_all_links()
    return render_template('directory.jinja', link_dicts=link_dicts)


def main(args):
    global links

    links = Links()

    app.run(
        host='0.0.0.0',
        debug=args.debug,
        port=args.port
    )


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