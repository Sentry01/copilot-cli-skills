#!/usr/bin/env python3
"""Install required Python packages for Excel operations."""
import subprocess, sys

PACKAGES = ["openpyxl", "pandas", "xlsxwriter", "matplotlib"]

def main():
    missing = []
    for pkg in PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if not missing:
        print("All dependencies already installed.")
        return 0
    
    print(f"Installing: {', '.join(missing)}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages"] + missing,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return 1
    print("Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
