#!/usr/bin/python
"""
Generate a simple web slideshow for use with a Chromecast.

Copyright (c) 2014 by Jim Lawless
See MIT/X11 license at
http://www.mailsend-online.com/license2014.php
"""

import argparse
import os
import SimpleHTTPServer
import SocketServer
import string

delay_millis = "10000"
html = ''


def open_in_browser(port):
    import webbrowser
    url = "http://localhost:" + str(port)
    webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a simple web '
                                     'slideshow for use with a Chromecast.')
    parser.add_argument(
        '-p', '--port', default=80, type=int,
        help='Port number.')
    parser.add_argument(
        '-d', '--delay', default=10, type=int,
        help='Delay in seconds between images.')
    parser.add_argument(
        '-b', '--browser', action='store_true',
        help="Automatically open the slideshow in a web browser.")
    args = parser.parse_args()

    images = os.listdir('img')

    # Build an HTML snippet that contains
    # a JavaScript list of string-literals.
    for img in images:
        if img in [".DS_Store"] or not os.path.isfile('img/' + img):
            continue
        html = html + '\"img/' + img + '\"'
        # Place a comma on the end
        # unless this is the last item in
        # the list
        if img != images[-1]:
            html = html + ','

    with open('template.htm', "r") as tplfile:
        payload = tplfile.read()

    # Replace $$1 and $$2 with the delay
    # in milliseconds and generated list
    # of images.  Write the output to
    # index.html
    payload = string.replace(payload, "$$1", str(args.delay * 1000))
    payload = string.replace(payload, "$$2", html)
    with open("index.html", "w") as indexfile:
        indexfile.write(payload)

    # Now, start serving up pages
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", args.port), Handler)
    print "HTTP server running..."
    if args.browser:
        open_in_browser(args.port)
    httpd.serve_forever()

# End of file
