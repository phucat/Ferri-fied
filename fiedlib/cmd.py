#!/usr/bin/env python2.7
import os
import argparse
import sys
import logging
import traceback
from tronlib import color_log
import xml.etree.ElementTree as ET

from slimit import minify


TEMPLATES_PATH = 'app/templates/'
STATIC_PATH = 'app/static/'
MIN_FILE_PATH = 'app/static/minified/'
FF_START = '<!--[FERRI-FY]-->'
FF_END = '<!--[FERRI-FIED]-->'


class Ferrified():

    FULL_JS_SOURCE = ''

    @classmethod
    def minify(self):
        minified = minify(self.FULL_JS_SOURCE, mangle=True, mangle_toplevel=True)
        logging.info(minified)

    @classmethod
    def compile_js(self, path):
        current_dir = os.path.abspath(os.getcwd())
        path = os.path.join(current_dir, STATIC_PATH + path)
        with open(path) as inputFile:
            self.FULL_JS_SOURCE += inputFile.read()

    @classmethod
    def parse_file(self, content, start_index, end_index):

        start_index = start_index + len(FF_START)
        scripts = content[start_index:end_index]
        #logging.warning('%s' % (scripts))
        tags = ET.fromstring('<f>%s</f>' % scripts)
        for item in tags:
            tag = item.tag.lower()
            if tag == 'script':
                src = item.get('src', None)
                if src:
                    self.compile_js(src)
                else:
                    self.FULL_JS_SOURCE += item.text
            elif tag == 'link':
                pass

        self.minify()

    @classmethod
    def get_html(self, file_path):
        if file_path.endswith('.html'):
            with open(file_path, 'r') as f:
                content = f.read()
                try:
                    start_indexes = list(self.find(content, FF_START))
                    end_indexes = list(self.find(content, FF_END))
                    for index in range(len(start_indexes)):
                        self.parse_file(content, start_indexes[index], end_indexes[index])
                except ValueError:
                    pass

    @classmethod
    def find(self, file, str):
        initial = 0
        while True:
            initial = file.find(str, initial)
            if initial == -1: return
            yield initial
            initial += len(str)


def main():
    parser = argparse.ArgumentParser(description='Tron handles communications with the Master Control Program.')
    subparsers = parser.add_subparsers(title='commands', help='valid commands')

    sparser = subparsers.add_parser('setup', help='Setup tron configuration')
    sparser.set_defaults(action='setup')
    sparser.add_argument('-s', '--show_current', action='store_true', help="Displays the current setup configuration.")

    current_dir = os.path.abspath(os.getcwd())
    logging.info("Ferris Directory : %s" % current_dir)

    path = os.path.join(current_dir, TEMPLATES_PATH)
    if os.path.exists(path):
        for root, _, files in os.walk(path):
            for f in files:
                Ferrified.get_html(os.path.join(root, f))


if __name__ == '__main__':
    main()
