Building
========

1. Install `python`
2. Create venv, install deps, and run
```
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -r requirements.txt
$ python src/core/simpleast.py src/core/test/expression.kool
```

# Example
Optimization pipeline for the following code snippet is shown below:
```
var a = 5, b = 6, c = 7
var d
while a > 0 {
    while b > 0 {
        b = b + 1
        while c > 0 {
            c = c + 1
            d = 9
        }
    }
}
```
## 1. Syntax Tree
![Tree](./img/tree.png)
## 2. Basic blocks
![BasicBlocks](./img/stage0.png)
## 3. Loop Invariant Code Motion
![LICM](./img/stage1.png)
![LICM1](./img/stage2.png)
![LICM2](./img/stage3.png)
## 4. Common Subexpression Elimination
![CSE](./img/stage4.png)
## 5. Copy Propagation
![CP](./img/stage5.png)
## 6. Constant Folding
![CF](./img/stage6.png)
## 7. Dead Code Elimination
![DCE](./img/stage7.png)
![DBE](./img/stage8.png)
