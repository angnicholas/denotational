---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Notebooks with MyST Markdown

Jupyter Book also lets you write text-based notebooks using MyST Markdown.
See [the Notebooks with MyST Markdown documentation](https://jupyterbook.org/file-types/myst-notebooks.html) for more detailed instructions.
This page shows off a notebook written in MyST Markdown.

## An example cell

With MyST Markdown, you can define code cells with a directive like so:

```{code-cell}
print(2 + 2)
```

When your book is built, the contents of any `{code-cell}` blocks will be
executed with your default Jupyter kernel, and their outputs will be displayed
in-line with the rest of your content.

```{seealso}
Jupyter Book uses [Jupytext](https://jupytext.readthedocs.io/en/latest/) to convert text-based files to notebooks, and can support [many other text-based notebook files](https://jupyterbook.org/file-types/jupytext.html).
```

## Create a notebook with MyST Markdown

MyST Markdown notebooks are defined by two things:

1. YAML metadata that is needed to understand if / how it should convert text files to notebooks (including information about the kernel needed).
   See the YAML at the top of this page for example.
2. The presence of `{code-cell}` directives, which will be executed with your book.

That's all that is needed to get started!

## Quickly add YAML metadata for MyST Notebooks

If you have a markdown file and you'd like to quickly add YAML metadata to it, so that Jupyter Book will treat it as a MyST Markdown Notebook, run the following command:

```
jupyter-book myst init path/to/markdownfile.md
```





### Tree Structure

```{graphviz}
digraph G {
    rankdir=TB;
    node [shape=box, style=filled, fontname="Times-Italic"];
    
    Add [label="Add", fillcolor=lightcoral];
    Int2 [label="Integer(2)", fillcolor=lightgreen];
    Mult [label="Multiply", fillcolor=lightblue];
    Int3 [label="Integer(3)", fillcolor=lightgreen];
    Int4 [label="Integer(4)", fillcolor=lightgreen];
    
    Add -> Int2 [label="left"];
    Add -> Mult [label="right"];
    Mult -> Int3 [label="left"];
    Mult -> Int4 [label="right"];
}
```

### Mathematical Denotation

The denotation function $\llbracket \cdot \rrbracket$ maps trees to integers:

$$\llbracket T \rrbracket = \begin{cases}
n & \text{if } T = \text{Integer}(n) \\
\llbracket T_1 \rrbracket + \llbracket T_2 \rrbracket & \text{if } T = \text{Add}(T_1, T_2) \\
\llbracket T_1 \rrbracket \times \llbracket T_2 \rrbracket & \text{if } T = \text{Multiply}(T_1, T_2)
\end{cases}$$

### Step-by-step Evaluation

$$\llbracket \text{Add}(\text{Integer}(2), \text{Multiply}(\text{Integer}(3), \text{Integer}(4))) \rrbracket$$

$$= \llbracket \text{Integer}(2) \rrbracket + \llbracket \text{Multiply}(\text{Integer}(3), \text{Integer}(4)) \rrbracket$$

$$= 2 + (\llbracket \text{Integer}(3) \rrbracket \times \llbracket \text{Integer}(4) \rrbracket)$$

$$= 2 + (3 \times 4) = 2 + 12 = 14$$

## Alternative Visualization Methods

### Using Mermaid for Simpler Trees

For simpler tree structures, you can also use Mermaid:

```{mermaid}
graph TD
    A["Add"] --> B["Integer(2)"]
    A --> C["Multiply"]
    C --> D["Integer(3)"]
    C --> E["Integer(4)"]
    
    style A fill:#ffcccc,stroke:#333,stroke-width:2px
    style C fill:#ccccff,stroke:#333,stroke-width:2px
    style B fill:#ccffcc,stroke:#333,stroke-width:2px
    style D fill:#ccffcc,stroke:#333,stroke-width:2px
    style E fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Advanced DOT with Mathematical Symbols

For more complex mathematical notation, you can use Unicode symbols or LaTeX-style notation in node labels:

```{graphviz}
digraph G {
    rankdir=TB;
    node [shape=box, style=filled, fontname="Times-Italic"];
    
    Add [label="+", fillcolor=lightcoral];
    Int2 [label="2", fillcolor=lightgreen];
    Mult [label="×", fillcolor=lightblue];
    Int3 [label="3", fillcolor=lightgreen];
    Int4 [label="4", fillcolor=lightgreen];
    
    Add -> Int2;
    Add -> Mult;
    Mult -> Int3;
    Mult -> Int4;
}
```

test test
