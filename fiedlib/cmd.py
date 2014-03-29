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
TEMPLATES_MIN_DIR = 'app/templates-min/'
STATIC_PATH = 'app/static/'
STATIC_MIN_DIR = 'app/static/ferri-fied/'
FF_START = '<!--[FERRI-FY]-->'
FF_END = '<!--[FERRI-FIED]-->'

DISCLAIMER = """
#===============================================\n
# Woolies Forms Portal\n
# All Right Reserved. Copyright 2014.\n
# Developed by Cloudsherpas\n
#===============================================
"""


def remove_js_comments(string):
    import re

    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string


class Ferrified():

    filename_in_process = None
    obfuscate = False

    full_js_source = ''
    full_css_source = ''
    full_hmtl_source = ''

    @classmethod
    def save_minified_source(self):
        path = os.path.join(self.current_dir, STATIC_MIN_DIR)
        files = []
        filename = self.filename_in_process
        if self.full_js_source:
            file_path = os.path.join(path, 'js/%s-ferrified.js' % filename)
            files.append(file_path)

        if self.full_css_source:
            file_path = os.path.join(path, 'css/%s-ferrified.css' % filename)
            files.append(file_path)

        for f in files:
            f = open(f, 'w')
            f.write("/*" + DISCLAIMER + "*/\n" + self.full_js_source)
            f.close()

        self.full_js_source = ''
        self.full_css_source = ''
        self.full_hmtl_source = ''

    @classmethod
    def minify(self):
        minified_js = minify(self.full_js_source, mangle=True, mangle_toplevel=True)
        self.full_js_source = minified_js

    @classmethod
    def compile_js(self, path):
        path = os.path.join(self.current_dir, STATIC_PATH + path)
        with open(path) as inputFile:
            source = remove_js_comments(inputFile.read())
            logging.info(source)
            self.full_js_source += " ".join(source.split())

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
                    self.full_js_source += item.text
            elif tag == 'link':
                pass

        if self.obfuscate:
            self.minify()

    @classmethod
    def save_template_min(self, root, _file):
        f = os.path.join(root, _file)
        with open(f, 'r') as f:
            content = " ".join(f.read().split())

        templates_min_dir = os.path.join(self.current_dir, TEMPLATES_MIN_DIR)
        current_dir_path, current_dir_name = os.path.split(root)
        path = templates_min_dir + '/' + current_dir_name
        if not os.path.isdir(path):
            os.makedirs(path)

        f = open("%s/%s" % (path, _file), 'w')
        f.write(content)
        f.close()

    @classmethod
    def find(self, file, str):
        initial = 0
        while True:
            initial = file.find(str, initial)
            if initial == -1: return
            yield initial
            initial += len(str)

    @classmethod
    def strip_html(self, file_path):
#        logging.info(file_path)
        self.filename_in_process = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, 'r') as f:
            content = f.read()

            start_indexes = list(self.find(content, FF_START))
            end_indexes = list(self.find(content, FF_END))
            for index in range(len(start_indexes)):
                self.parse_file(content, start_indexes[index], end_indexes[index])

            self.save_minified_source()

    @classmethod
    def create_directories(self):

        min_dir = os.path.join(self.current_dir, STATIC_MIN_DIR)
        if not os.path.isdir(min_dir):
            os.makedirs(os.path.join(min_dir))

        js_min_dir = min_dir + "/js"
        if not os.path.isdir(js_min_dir):
            os.makedirs(js_min_dir)

        css_min_dir = min_dir + "/css"
        if not os.path.isdir(css_min_dir):
            os.makedirs(css_min_dir)

        templates_min_dir = os.path.join(self.current_dir, TEMPLATES_MIN_DIR)
        if not os.path.isdir(templates_min_dir):
            os.makedirs(templates_min_dir)

    @classmethod
    def init(self, path):
        self.current_dir = path
        self.create_directories()

        path = os.path.join(self.current_dir, TEMPLATES_PATH)
        if os.path.exists(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith('.html'):
                        Ferrified.strip_html(os.path.join(root, f))
                        self.save_template_min(root, f)


def main():
    parser = argparse.ArgumentParser(description='Tron handles communications with the Master Control Program.')
    subparsers = parser.add_subparsers(title='commands', help='valid commands')

    sparser = subparsers.add_parser('setup', help='Setup tron configuration')
    sparser.set_defaults(action='setup')
    sparser.add_argument('-s', '--show_current', action='store_true', help="Displays the current setup configuration.")

    current_dir = os.path.abspath(os.getcwd())
    Ferrified.init(current_dir)
    logging.info("Ferris Directory : %s" % current_dir)


if __name__ == '__main__':
    main()
