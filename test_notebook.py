#!/usr/bin/env python3
"""
Test script to verify the interactive notebook works correctly.
"""

import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def test_notebook():
    """Test the interactive notebook by executing it."""
    print("🧪 Testing Interactive Notebook")
    print("=" * 40)

    # Read the notebook
    with open("denotational/interactive-demos.ipynb", "r") as f:
        nb = nbformat.read(f, as_version=4)

    # Execute the notebook
    ep = ExecutePreprocessor(timeout=300, kernel_name="python3")

    try:
        ep.preprocess(nb, {"metadata": {"path": "denotational/"}})
        print("✅ Notebook executed successfully!")

        # Check if widgets were generated
        widget_cells = 0
        for cell in nb.cells:
            if cell.cell_type == "code" and "widgets" in cell.source:
                widget_cells += 1

        print(f"📊 Found {widget_cells} cells with widgets")

        # Save the executed notebook
        with open("denotational/interactive-demos.ipynb", "w") as f:
            nbformat.write(nb, f)

        print("💾 Executed notebook saved")
        return True

    except Exception as e:
        print(f"❌ Error executing notebook: {e}")
        return False


if __name__ == "__main__":
    success = test_notebook()
    sys.exit(0 if success else 1)
