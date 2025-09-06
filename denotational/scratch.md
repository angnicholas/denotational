
Semantics decouples (cf SOLID, OOP/SWE principles) the logic of proving correctness of a program from proving the correctness of your language compiler 

Ie. 

If you wanted to prove that your Python implementation of Floyd Warshall works, you have to know Floyd Warshall works, and that your Python interpreter works.

If you do that each time, it's coupled.

So we prove that Python works one time, and then we can use (cf Algorithms course-style proofs) for Floyd Warshall.

To prove that Python works, we need to formally define the behaviour of any python program 

And that is semantics.








- Introduce programs
- Introduce denotation as what the program should resolve to
- Introduce functions as deferred computation
- But limited by depth of abstraction - want to make depth user-controlled (eg. ackerman)
- That introduces the possibility of infinite loops which have zero informational content

---
Then,



Recursion

If we are given a recursive definition, it is difficult to figure out what it does.

But if suppose the heavens open and a voice spoke to us that `fib` computes fibonacci, it is easy to deduce that that's correct by traversing the tree and seeing that it doesn't change. Then we can convince ourselves that `fib` does indeed compute fibonacci

---

How do we formalise this intuition?

We can use a slightly different construct to give us recursion (makes it easier to reason about its function, although more clunky to program in).

That's the **fixpoint operator**, and it roughly translates to

Suppose I have a transformation T, that acts on a table f to produce a new table g. `fix(T)` refers to the special table, f star, such that applying the transformation T does not change any of its entries.

And the bold claim is that to "derive" fix T for any T, I can start at the table filled with bottoms, and keep applying T to it until the table stops changing.

It provides another aspect of looking at recursion. 



 construct as the 

Idea: Assume that your program never terminates on all inputs.

Yes: Assume that your program never terminates. And the

If we know that `fib` computes the fibonacci function, we can verify that it works by tracking its tree and seeing that it doesn't change.


