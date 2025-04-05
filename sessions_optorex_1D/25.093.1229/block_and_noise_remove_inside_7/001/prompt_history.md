
## train_1

**input:**
```
5 5 5 5 5 1 5 5 5 5 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 0 0
```


## train_2

**input:**
```
2 2 2 2 2 2 2 2 3 2 2 2
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2
```


## train_3

**input:**
```
0 0 0 0 5 5 5 5 5 5 5 4
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5
```


## train_4

**input:**
```
0 9 5 9 9 9 9 9 9 9 4 2
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 9 9
```


## train_5

**input:**
```
5 5 5 5 5 5 5 3 5 5 5 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 5 0
```


## train_6

**input:**
```
0 0 1 1 1 1 1 1 1 1 9 1
```


**output:**
```
0 0 1 1 1 1 1 1 1 1 1 1
```


## train_7

**input:**
```
0 0 5 5 5 5 5 5 5 5 6 1
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5
```

*   **Perception of task elements:**
    *   The input and output are both sequences of single-digit integers, presented as space-separated strings.
    *   The length of the sequence remains constant from input to output (12 elements in all provided examples).
    *   The core task is to modify certain elements within the sequence based on the values of their adjacent elements.
    *   The number `0` appears to be static; it never changes its value and does not seem to influence its neighbors' changes.
    *   Non-zero numbers can
