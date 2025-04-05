
## train_1

**input:**
```
0 8 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 0 0 8
```


## train_2

**input:**
```
0 8 8 8 8 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 8 8 8 8 0 0
```


## train_3

**input:**
```
0 0 0 0 0 2 5 5 5 0 0 0
```


**output:**
```
0 0 5 5 5 2 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 2 9 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 2 0 0 0
```


## train_5

**input:**
```
0 5 5 0 0 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 0 0 5 5 0 0
```


## train_6

**input:**
```
0 7 7 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 0 7 7
```


## train_7

**input:**
```
0 0 0 0 0 0 2 0 7 0 0 0
```


**output:**
```
0 0 0 0 7 0 2 0 0 0 0 0
```

## Perception

1.  **Input/Output Format:** Both input and output are fixed-length sequences (lists) of 12 integers.
2.  **Key Elements:** The sequences contain the integer `0`, the integer `2`, and other single-digit positive integers (e.g., 5, 7, 8, 9).
3.  **Invariant Element:** The integer `2` appears exactly once in each input and output sequence. Crucially, its position (index) within the sequence remains unchanged from input to output.
4.  **Mobile Elements:** The non-zero integers other than `2` change their positions. `0`s act as placeholders or padding.
5.  **Transformation Pattern:** The number `2` acts as a pivot or separator. The block of non-zero numbers (excluding `2`) found *before* the `2` in the input sequence is moved to occupy the positions *after* the `2` in the output sequence. Conversely, the block of non-zero numbers found *after* the `2` in the input sequence is moved to occupy the positions *before* the `2` in the output sequence.
6.  **Order Preservation:** Within the block of numbers moved from before `2` to after `2`, their relative order is preserved. Similarly, the relative order is preserved for the numbers moved from after `2` to before `2`.
7.  **Padding:** Zeros (`0`) fill all positions in the output sequence not occupied by the `2` or the relocated non-zero numbers. The placement ensures the moved blocks are adjacent to the `2`.

## Facts


```yaml
task_type: sequence_transformation
input_format:
  type: list
  element_type: integer
  length: 12
output_format:
  type: list
  element_type: integer
  length: 12
elements:
  - type: pivot
    value: 2
    properties:
      - count: 1 per sequence
      - position: invariant between input and output
  - type: mobile
    value: non-zero integers other than 2
    properties:
      - relocation: position changes based on pivot
      - relative_order: preserved within relocated groups
  - type: padding
    value: 0
    properties:
      - fills empty spaces
transformation:
  actions:
    - find the index 'p' of the pivot element '2'
    - extract non-zero elements before index 'p' into list 'B', preserving order
    - extract non-zero elements after index 'p' into list 'A', preserving order
    - construct output list of length 12, initialized with padding element '0'
    - place pivot element '2' at index 'p' in the output list
    - place elements from list 'A' into the output list immediately before index 'p' (i.e., at indices p - len(A) to p - 1)
    - place elements from list 'B' into the output list immediately after index 'p' (i.e., at indices p + 1 to p + len(B))
  relationship:
    - non-zero elements swap sides relative to the pivot '2'
```


## Natural Language Program

1.  Identify the input sequence of 12 integers.
2.  Locate the index (position) of the integer `2`. Let this index be `p`.
3.  Create a new, empty list called `before_elements`. Iterate through the input sequence from the beginning up to (but not including) index `p`. If an element is not zero, append it to `before_elements`.
4.  Create another new, empty list called `after_elements`. Iterate through the input sequence starting from the element after index `p` until the end. If an element is not zero, append it to `after_elements`.
5.  Initialize an output sequence of 12 integers, filling all positions with `0`.
6.  Place the integer `2` into the output sequence at index `p`.
7.  Place the contents of the `after_elements` list into the output sequence, ending at index `p-1`. Specifically, they occupy indices from `p - length(after_elements)` to `p - 1`.
8.  Place the contents of the `before_elements` list into the output sequence, starting at index `p+1`. Specifically, they occupy indices from `p + 1` to `p + length(before_elements)`.
9.  The resulting sequence is the final output.
