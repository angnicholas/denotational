#!/usr/bin/env python3
"""
Script to build the Jupyter Book with interactive widgets support.
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'=' * 50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'=' * 50}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Error!")
        print("Return code:", e.returncode)
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False


def main():
    """Main function to build the book."""
    print("🚀 Building Jupyter Book with Interactive Widgets")
    print("=" * 60)

    # Change to the denotational directory
    os.chdir("denotational")

    # Step 1: Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("Failed to install requirements. Please check your Python environment.")
        return False

    # Step 2: Enable Jupyter widgets extension
    if not run_command("jupyter nbextension enable --py widgetsnbextension --sys-prefix", "Enabling Jupyter widgets extension"):
        print("Warning: Could not enable widgets extension. Widgets may not work properly.")

    # Step 3: Enable JupyterLab widgets extension
    if not run_command("jupyter labextension install @jupyter-widgets/jupyterlab-manager", "Enabling JupyterLab widgets extension"):
        print("Warning: Could not enable JupyterLab widgets extension.")

    # Step 4: Execute the interactive notebook first to generate outputs
    print("\n📝 Executing interactive notebook to generate widget outputs...")
    if not run_command(
        "jupyter nbconvert --to notebook --execute interactive-demos.ipynb --output interactive-demos.ipynb",
        "Executing interactive notebook",
    ):
        print("Warning: Could not execute interactive notebook. Widgets may not display properly.")

    # Step 5: Build the book
    if not run_command("jupyter-book build .", "Building Jupyter Book"):
        print("Failed to build the book.")
        return False

    print("\n🎉 Book built successfully!")
    print("\nTo view the book:")
    print("1. Open a terminal in the denotational directory")
    print("2. Run: python -m http.server 8000")
    print("3. Open your browser to: http://localhost:8000/_build/html/index.html")
    print("\nOr simply open: denotational/_build/html/index.html in your browser")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
