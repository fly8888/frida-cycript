#!/usr/bin/env python
from __future__ import print_function

import codecs
import subprocess
import sys

host_os = sys.argv[1]
host_arch = sys.argv[2]
analyze = sys.argv[3]
analysis_cpp = sys.argv[4]
bridge_old = sys.argv[5]
output_file = sys.argv[6]
extra_flags = sys.argv[7:]

host_clang_arch = 'i386' if host_arch == 'x86' else host_arch

host_flags = []

if host_os == 'macos':
    sdk = 'macosx'
    minver = '10.9'

    sdk_path = subprocess.check_output(["xcrun", "--sdk", sdk, "--show-sdk-path"]).strip()

    host_flags = [
        "-ObjC++",
        "-isysroot", sdk_path,
        "-mmacosx-version-min=" + minver,
        "-arch", host_clang_arch,
        "-stdlib=libc++",
    ]
elif host_os == 'ios':
    sdk = 'iphoneos'
    minver = '7.0'

    sdk_path = subprocess.check_output(["xcrun", "--sdk", sdk, "--show-sdk-path"]).strip()

    host_flags = [
        "-ObjC++",
        "-isysroot", sdk_path,
        "-miphoneos-version-min=" + minver,
        "-arch", host_clang_arch,
        "-stdlib=libc++"
    ]

analyze_args = [
    analyze,
    analysis_cpp,
] + host_flags + extra_flags
print("analyze_args:", " ".join(analyze_args))
definitions = subprocess.check_output(analyze_args).decode('utf-8')

with codecs.open(bridge_old, 'r', 'utf-8') as f:
    old_definitions = f.read()

with codecs.open(output_file, 'w', 'utf-8') as f:
    f.write(definitions + old_definitions)
