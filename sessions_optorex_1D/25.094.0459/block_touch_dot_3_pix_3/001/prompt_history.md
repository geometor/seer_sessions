
## train_1

**input:**
```
0 0 9 9 9 9 9 9 0 0 0 2
```


**output:**
```
0 0 0 0 0 9 9 9 9 9 9 2
```


## train_2

**input:**
```
3 3 3 3 3 3 3 0 0 0 0 2
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 0 2
```


## train_3

**input:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


**output:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


## train_4

**input:**
```
0 0 0 2 0 0 5 5 5 5 5 5
```


**output:**
```
0 0 0 2 5 5 5 5 5 5 0 0
```


## train_5

**input:**
```
0 4 4 4 4 4 4 4 0 0 2 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 2 0
```


## train_6

**input:**
```
0 0 0 0 0 0 2 0 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 2 8 8 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 2 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 2 5 5 5
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

*   **Input/Output Format:** Both input and output are sequences of single-digit integers, presented as space-separated strings.
*   **Key Element (`2`):** The digit `2` appears to play a crucial role. It acts as a stable pivot or separator in the sequence. Its position doesn't change relative to the rearrangement happening around it.
*   **Mobile Element (`0`):** The digit `0` is the element being moved. Its final position depends on whether it initially appeared before or after the first `2`.
*   **Other Elements (Non-zero, Non-two):** Digits other than `0` and `2` seem to maintain their relative order within their respective sections (before or after the `2`) but shift their absolute positions to accommodate the moved `0`s.
*   **Transformation:** The transformation involves partitioning the sequence based on the first `2` and then rearranging the `0`s within those partitions. Zeros originally before the `2` congregate at the beginning of the pre-`2` section. Zeros originally after the `2` congregate at the end of the post-`2` section.

**YAML Facts:**


