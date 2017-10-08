#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import logging
import os
from re import search
from yaml import load, dump


# global vars
genealogy = []

loglevel = str(os.environ.get('LOGLEVEL', 'WARNING'))
logformat = '%(asctime)s %(levelname)s: %(message)s'

if loglevel == 'DEBUG':
    loglevel = logging.DEBUG
elif loglevel == 'INFO':
    loglevel = logging.INFO
elif loglevel == 'WARNING':
    loglevel = logging.WARNING
else:
    loglevel = logging.ERROR

logging.basicConfig(format=logformat, level=loglevel)


def search_path(input, a):
    l = input.split('/')
    if len(l) > 1:
        d = "/".join(l[:-1])
        a.append(d)
        search_path(d, a)
    return a


def get_registries(path):
    r = []
    registries = []
    try:
        registries += load(open(path + '/registries.yml'))
    except:
        logging.debug('Did not find registries.yml in ' + path)

    paths = search_path(path, r)
    for p in paths:
        try:
            registries += load(open(p + '/registries.yml'))
        except:
            logging.debug('Did not find registries.yml in ' + path)
    # return only unique values in case there are duplicates
    return list(set(registries))


def find_file_paths(filename, path='./'):
    # import glob
    # files = glob.glob("./**/%s" % filename, recursive=True) # python 3.5+
    file_paths = []
    for root, dirnames, filenames in os.walk(path):
        for f in fnmatch.filter(filenames, filename):
            file_paths.append(os.path.join(root, f))
    return file_paths


def scrub_path_name(path_name):
    x = path_name.replace('./', '')
    x = x.split('/')
    # remove null items
    x = [ i for i in x if i ]
    return '-'.join(x)


def get_name(path, registries):
    # separate name and registry from path
    for r in registries:
        if r in path:
            path = path.replace(r, '')
    return scrub_path_name(path)


def add_container(dockerfile, from_container):
    c = dict()
    c['directory'] = os.path.dirname(dockerfile)
    c['from_container'] = from_container
    c['registries'] = get_registries(os.path.dirname(dockerfile))
    c['name'] = get_name(c['directory'], c['registries'])
    global genealogy
    genealogy.append(c)


def main():
    containers = find_file_paths('Dockerfile')

    for c in containers:
        with open(c) as f:
            for line in f:
                # [a-z0-9]+(?:[._-][a-z0-9]+)*  https://docs.docker.com/registry/spec/api/
                match = search('^FROM\s([a-z0-9]+(:?)([\._\-a-z0-9]+)*)', line)
                if match:
                  logging.info(match.groups())
                  add_container(c, match.group(1))

    with open('container-schematic.yml', 'w') as outfile:
        dump(genealogy, outfile, default_flow_style=False)
    logging.debug("\n\n" + dump(load(open('container-schematic.yml')), default_flow_style=False))

if __name__ == '__main__':
    main()
