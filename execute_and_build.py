#!/usr/bin/env python3
"""
Simple script to execute the interactive notebook and build the book.
"""

import os
import subprocess
import sys


def main():
    print("🚀 Executing Interactive Notebook and Building Jupyter Book")
    print("=" * 60)

    # Change to the denotational directory
    os.chdir("denotational")

    # Step 1: Install requirements
    print("\n📦 Installing requirements...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

    # Step 2: Execute the notebook to generate outputs
    print("\n📝 Executing interactive notebook...")
    try:
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "interactive-demos.ipynb",
                "--output",
                "interactive-demos.ipynb",
                "--ExecutePreprocessor.timeout=300",
            ],
            check=True,
        )
        print("✅ Notebook executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing notebook: {e}")
        print("Continuing with build anyway...")

    # Step 3: Build the book
    print("\n📚 Building Jupyter Book...")
    try:
        subprocess.run(["jupyter-book", "build", "."], check=True)
        print("✅ Book built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building book: {e}")
        return False

    print("\n🎉 All done!")
    print("\nTo view your book:")
    print("1. Open: denotational/_build/html/index.html in your browser")
    print("2. Or run: cd denotational/_build/html && python -m http.server 8000")
    print("   Then visit: http://localhost:8000")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
