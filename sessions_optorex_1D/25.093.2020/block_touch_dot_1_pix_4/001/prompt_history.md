
## train_1

**input:**
```
0 3 3 3 3 3 3 3 3 2 0 0
```


**output:**
```
0 3 3 3 3 3 3 3 3 2 0 0
```


## train_2

**input:**
```
0 0 0 0 0 6 6 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 6 2 0 0 0 0
```


## train_3

**input:**
```
2 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
2 3 3 3 3 3 3 0 0 0 0 0
```


## train_4

**input:**
```
5 5 5 5 5 5 5 5 5 5 2 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 2 0
```


## train_5

**input:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


**output:**
```
0 0 0 2 4 4 4 4 4 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 9 9 9 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 0 2
```


## train_7

**input:**
```
4 0 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 2 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves transforming a sequence of single-digit integers into another sequence of the same length.
Observing the training examples:
- Most examples (train_1 to train_5) show the output being identical to the input.
- train_6 and train_7 show a change.
    - In train_6: `... 0 0 9 ...` becomes `... 0 0 0 9 ...`. It looks like a `0` that was immediately followed by a non-zero number (`9`) has moved one position to the left, swapping with its left neighbor (which was also `0`).
    - In train_7: `4 0 2 ...` becomes `0 4 2 ...`. Here, a `0` that was immediately followed by a non-zero number (`2`) has moved one position to the left, swapping with its left neighbor (`4`).
- The common pattern in the modified examples (train_6, train_7) seems to be locating the *first* instance of a `0` that is immediately followed by a non-zero digit. If such a `0` exists and it's not the very first element in the sequence, it swaps positions with the element immediately to its left.
- In the examples where no change occurs (train_1 to train_5), either there is no `0` followed by a non-zero digit (train_3, train_4), or the first such `0` is already at the beginning of the sequence (train_1), or swapping it with its left neighbor results in no visible change because the neighbor is also `0` (train_2, train_5).

## Facts


```yaml
objects:
  - name: sequence
    type: list of integers
    description: The input and output data structures.
  - name: element
    type: integer
    description: Individual numbers within the sequence.
properties:
  - object: element
    name: value
    type: integer
    description: The numerical value of the element (0-9).
  - object: element
    name: index
    type: integer
    description: The position of the element within the sequence (zero-based).
  - object: element
    name: is_zero
    type: boolean
    description: True if the element's value is 0.
  - object: element
    name: is_non_zero
    type: boolean
    description: True if the element's value is not 0.
relationships:
  - type: adjacency
    description: Elements can be adjacent (left neighbor, right neighbor) within the sequence.
    properties:
      - element_1: index i
      - element_2: index i+1 (right neighbor)
      - element_3: index i-1 (left neighbor)
actions:
  - name: scan
    description: Iterate through the sequence elements from left to right.
  - name: find_pattern
    description: Locate the first index `i` where element `i` is 0 and element `i+1` is non-zero.
    condition: Requires checking pairs of adjacent elements.
  - name: swap
    description: Exchange the positions of two elements in the sequence.
    condition: Applicable if the pattern is found at index `i > 0`. Swaps elements at `i` and `i-1`.
  - name: no_change
    description: The sequence remains unaltered.
    condition: Applicable if the pattern is not found, or if the pattern is found at index `i = 0`.
```


## Natural Language Program

1.  Iterate through the input sequence from the first element up to the second-to-last element. Let the current index be `i`.
2.  At each index `i`, check if the element at `i` is `0` AND the element at the next index `i+1` is non-zero.
3.  If this condition is met for the first time at index `i`:
    a.  Check if `i` is greater than 0 (i.e., the found `0` is not the very first element of the sequence).
    b.  If `i > 0`, swap the element at index `i` with the element at index `i-1`.
    c.  Stop iterating, as the transformation involves only the *first* occurrence of the pattern.
4.  If the condition in step 2 is never met, or if it's met only at index `i = 0`, make no changes to the sequence.
5.  Output the resulting sequence.
