#!/usr/bin/env python

import codecs
import os
import subprocess
import sys

def fixup(source_path):
    with codecs.open(source_path, 'rb', 'utf-8') as f:
        code = f.read().replace('yytranslate_ (yylex (', '(yylex_ (')
    with codecs.open(source_path, 'wb', 'utf-8') as f:
        f.write(code)

bison = sys.argv[1]
grammar = sys.argv[2]
output_header = sys.argv[3]
output_source = sys.argv[4]

output_dir = os.path.dirname(output_source)

bison_args = [
    bison,
    "-v",
    "--report=state",
    "-Werror",
    "-o", os.path.basename(output_source),
    os.path.relpath(grammar, output_dir)
]
subprocess.check_call(bison_args, cwd=output_dir)

fixup(output_source)
