#!/usr/bin/env python

import shutil
import subprocess
import sys

npm = sys.argv[1]
package_json = sys.argv[2]
output_dir = sys.argv[3]

shutil.copy(package_json, output_dir)
process = subprocess.Popen([npm, "install"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=output_dir)
(stdout_data, stderr_data) = process.communicate()
exit_code = process.returncode
if exit_code != 0:
    sys.stderr.write(stdout_data)
sys.exit(exit_code)
