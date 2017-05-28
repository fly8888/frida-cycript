#!/usr/bin/env python

import codecs
import os
import re
import sys

include_pattern = re.compile(r'^@include (.+)$')
begin_pattern = re.compile(r'^@begin (.+)$')
end_pattern = re.compile(r'^@end$')

def include(source, output_file, filters):
    condition = []
    for line in codecs.open(source, 'rb', 'utf-8'):
        line = line.rstrip()

        handled = False
        if len(line) > 0 and line[0] == '@':
            if not handled:
                match = include_pattern.match(line)
                if match is not None:
                    other_source = os.path.join(os.path.dirname(source), match.group(1))
                    include(other_source, output_file, filters)
                    handled = True

            if not handled:
                match = begin_pattern.match(line)
                if match is not None:
                    requirement = match.group(1)
                    condition.append(lambda: requirement in filters)
                    handled = True

            if not handled:
                match = end_pattern.match(line)
                if match is not None:
                    condition.pop()
                    handled = True

        if not handled and (len(condition) == 0 or condition[-1]()):
            output_file.write(line)
            output_file.write('\n')

input_path = sys.argv[1]
output_path = sys.argv[2]
filters = set(sys.argv[3:])

with codecs.open(output_path, 'wb', 'utf-8') as output_file:
    include(input_path, output_file, filters)
