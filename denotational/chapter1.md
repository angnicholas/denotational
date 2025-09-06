# Chapter 1. Programs

You might have heard semantics being referred to as "giving meaning to programs", and denotational semantics the task of "assigning mathematical objects to programs". While this is mostly accurate, it sometimes can get confusing what "meaning" really means, what is a "program", and what is a "mathematical object".

## Programs as "tagged-trees"

When we write code (Python, Java, etc...), we think of ourselves as entering a bunch of commands, and some kind of computation "magically-happens", due to the action of the compiler/interpreter.  

But imagine you are now tasked with writing a compiler/interpreter. The input (which is the program you are compiling / interpreting) is just a **plain-text file** - or more precisely, an **abstract-syntax tree** (AST) obtained after parsing the plaintext.  

A good way to visualise this is the [Scratch Programming Language](https://miro.medium.com/v2/resize:fit:4800/format:webp/0*FI4oCrDhbyc-HQ-Z.png) where you have these blocks that you compose together. The blocks are "tagged" - in the sense that they could be an if-then-else block, a while block, etc., and the blocks can store some data (eg. the integer "2").  

This means that a program (in virtually every single programming language) is a tree data structure, consisting of tagged nodes, that each represent some sort of computational unit. These nodes **compose** to build larger computational units.  

Now the whole point of building a compiler/interpreter/evaluator is to do meaningful computation with the trees. That is, we want to build a machine, M, (let's call him Mike), that consumes *any* given tree, and spits out a result, that should align with the computational result which the tree is trying to represent. Let us visualise this with an example.

## Build a calculator

Let us introduce our first node, which we will call the `Integer` node. This is a node that simply represents an integer, eg. "5", and has no children

Alongside this, we will introduce two other nodes, `Add` and `Multiply`. These nodes do not have data, but have two children, and encode the arithmetic operations of Add and Multiply respectively.  

In a syntactic form, we define `Tree` with the following syntax:
```
Tree = Integer | Add | Multiply
Integer = 0 | 1 | 2 | 3 ...
Add = Tree * Tree
Multiply = Tree * Tree
```

Remember that Mike's task is to take an arbitrary tree as input and produce a computation result. In this case, it is pretty obvious that the computation result should be an integer. 

If we give precise instructions to Mike as to how he should do this, it will look something like:

1. Look up the tag of the root of the tree
    a. If the tag is `Integer`, return the value that it holds.
    b. If the tag is `Add`, perform the computation on both branches, add the two results together and return it.
    c. If the tag is `Multiply`, perform the computation on both branches, multiply the two results together and return it.






Topics

Apart from those on the board












## Visualizing Tree Denotation

Let's visualize the tree structure and its denotation. Consider the expression `2 + (3 × 4)`:
