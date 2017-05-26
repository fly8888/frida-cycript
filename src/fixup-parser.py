#!/usr/bin/env python

import codecs
import sys

source_path = sys.argv[1]
with codecs.open(source_path, 'rb', 'utf-8') as f:
    code = f.read().replace('yytranslate_ (yylex (', '(yylex_ (')
with codecs.open(source_path, 'wb', 'utf-8') as f:
    f.write(code)
