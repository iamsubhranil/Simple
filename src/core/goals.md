1. A simple, dynamically typed language with basic assignments, expressions, and if and while control flow operations (Done)
    1. Assignment statements are not usable expressions
    2. An expression statement only contains assignments
    3. Any number != boolean
2. Generation of three address code from a program (Done)
3. Generation of basic blocks from the three address code (Done)
4. Creating CFG from basic blocks (Done)
5. Performing optimizations
    1. Constant folding using reaching definitions (done)
    2. Copy propagation using reaching definitions (done)
    3. Common subexpression elimination using available expressions (done)
    4. Dead code elimination using liveness analysis (done)
    5. Unreachable code elimination (done)
    6. Loop invariant code motion (done)
    7. Peephole optimizations (Strength reduction)
    8. Loop unrolling
6. No function calls, no objects until all goals are completed
