#!/usr/bin/env python3
"""
Setup script for Thebe integration with Jupyter Book.
This script helps configure Thebe for executable cells.
"""

import os
import subprocess
import sys

import yaml


def update_config_for_thebe():
    """Update _config.yml to include Thebe configuration."""
    config_path = "denotational/_config.yml"

    # Read current config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Add Thebe configuration
    if "sphinx" not in config:
        config["sphinx"] = {}

    if "config" not in config["sphinx"]:
        config["sphinx"]["config"] = {}

    # Add Thebe config
    config["sphinx"]["config"]["thebe_config"] = {
        "repository_url": "https://github.com/YOUR_USERNAME/YOUR_REPO",
        "repository_branch": "master",
        "binderhub_url": "https://mybinder.org",
        "selector": ".thebe-init",
        "kernel_name": "python3",
    }

    # Update HTML config
    if "html" not in config:
        config["html"] = {}

    config["html"]["extra_navbar"] = """
    <div class="navbar-nav">
      <a class="nav-link" href="https://mybinder.org/v2/gh/YOUR_USERNAME/YOUR_REPO/master?urlpath=tree/docs">
        <i class="fas fa-external-link-alt"></i> Launch Binder
      </a>
    </div>
    """

    # Write updated config
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print("✅ Updated _config.yml with Thebe configuration")
    print("⚠️  Remember to replace 'YOUR_USERNAME/YOUR_REPO' with your actual GitHub repository!")


def create_binder_requirements():
    """Create requirements.txt for Binder."""
    requirements = """jupyter-book
matplotlib
networkx
numpy
ipywidgets
jupyter
notebook
ipykernel
sphinx-thebe
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements)

    print("✅ Created requirements.txt for Binder")


def create_binder_postbuild():
    """Create postBuild script for Binder."""
    postbuild = """#!/bin/bash
# Enable Jupyter widgets
jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
"""

    with open("postBuild", "w") as f:
        f.write(postbuild)

    # Make it executable
    os.chmod("postBuild", 0o755)

    print("✅ Created postBuild script for Binder")


def main():
    """Main setup function."""
    print("🚀 Setting up Thebe for Jupyter Book")
    print("=" * 50)

    # Change to project directory
    os.chdir("denotational")

    # Update configuration
    update_config_for_thebe()

    # Go back to parent directory for Binder files
    os.chdir("..")

    # Create Binder files
    create_binder_requirements()
    create_binder_postbuild()

    print("\n🎉 Thebe setup complete!")
    print("\nNext steps:")
    print("1. Replace 'YOUR_USERNAME/YOUR_REPO' in _config.yml with your actual GitHub repository")
    print("2. Push your code to GitHub")
    print("3. Build your book: jupyter-book build denotational/")
    print("4. Deploy to GitHub Pages or any static hosting service")
    print("\nYour readers will then be able to run code cells directly in the browser!")


if __name__ == "__main__":
    main()
