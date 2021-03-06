#
# Copyright (c) Dell Inc., or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

from __future__ import division
import os
import json
import yaml
import bz2
import codecs
from contextlib import closing

def load_json_from_file(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.bz2':
        with closing(bz2.BZ2File(filename, 'rb')) as data_file:
            reader = codecs.getreader("utf-8")
            data = json.load(reader(data_file))
    elif ext == '.yaml':
        with open(filename) as data_file:
            data = yaml.full_load(data_file)
    else:
        with open(filename) as data_file:
            data = json.load(data_file)
    return data

def save_json_to_file(data, filename, sort_keys=False, indent=None, ensure_ascii=False):
    ext = os.path.splitext(filename)[1]
    temp_file_name = '%s.tmp%s' % os.path.splitext(filename)    
    if ext == '.bz2':
        with closing(bz2.BZ2File(temp_file_name, 'wb')) as data_file:
            s = json.dumps(data, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)
            data_file.write(s.encode())
    else:
        with open(temp_file_name, 'w') as data_file:
            json.dump(data, data_file, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)
    os.rename(temp_file_name, filename)
    
def append_to_json_file(data, filename, sort_keys=False, indent=None, ensure_ascii=False):
    recs = []
    if os.path.exists(filename):
        recs.extend(load_json_from_file(filename))
    recs.extend(data)
    save_json_to_file(recs, filename, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)   
