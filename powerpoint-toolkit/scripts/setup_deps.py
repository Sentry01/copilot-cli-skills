#!/usr/bin/env python3
"""Install required Python packages for PowerPoint operations."""
import subprocess, sys

PACKAGES = ["python-pptx", "Pillow", "pyyaml"]

def main():
    missing = []
    import_names = {"python-pptx": "pptx", "Pillow": "PIL", "pyyaml": "yaml"}
    for pkg in PACKAGES:
        try:
            __import__(import_names.get(pkg, pkg))
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
