#!/usr/bin/env python3
"""Compare the star growth of popular frontend frameworks."""

import subprocess
import sys

repos = [
    "facebook/react",
    "vuejs/vue",
    "sveltejs/svelte",
    "angular/angular",
]

print("Comparing frontend frameworks...\n")
for repo in repos:
    subprocess.run([sys.executable, "star_history.py", repo, "--summary"])
    print()
