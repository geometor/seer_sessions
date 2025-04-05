
## train_1

**input:**
```
3 3 3 3 3 0 0 3 3 3 3 0
```


**output:**
```
1 1 1 1 1 0 0 2 2 2 2 0
```


## train_2

**input:**
```
0 0 3 3 3 0 3 3 3 3 3 0
```


**output:**
```
0 0 2 2 2 0 1 1 1 1 1 0
```


## train_3

**input:**
```
0 3 3 0 0 0 3 3 3 3 3 0
```


**output:**
```
0 2 2 0 0 0 1 1 1 1 1 0
```


## train_4

**input:**
```
0 3 3 3 3 0 0 0 0 3 3 0
```


**output:**
```
0 1 1 1 1 0 0 0 0 2 2 0
```


## train_5

**input:**
```
0 0 0 0 0 3 3 0 0 3 3 3
```


**output:**
```
0 0 0 0 0 2 2 0 0 1 1 1
```


## train_6

**input:**
```
0 0 0 0 3 3 0 3 3 3 0 0
```


**output:**
```
0 0 0 0 2 2 0 1 1 1 0 0
```


## train_7

**input:**
```
3 3 3 3 3 0 3 3 3 0 0 0
```


**output:**
```
1 1 1 1 1 0 2 2 2 0 0 0
```

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are sequences of single-digit integers represented as space-separated strings.
2.  **Sequence Length:** The length of the output sequence is identical to the length of the input sequence in all examples.
3.  **Value Mapping:**
    *   The integer `0` in the input always maps to `0` in the output at the corresponding position.
    *   The integer `3` in the input maps to either `1` or `2` in the output.
4.  **Block Transformation:** The transformation of `3` depends on its position within contiguous blocks of `3`s. These blocks are separated by `0`s.
5.  **Order Dependence:** The mapping of a block of `3`s (to `1`s or `2`s) is determined by the order in which that block appears when scanning the input sequence from left to right.
    *   The first encountered contiguous block of `3`s is transformed into a block of `1`s of the same length.
    *   The second encountered contiguous block of `3`s is transformed into a block of `2`s of the same length.
6.  **Scope:** All provided examples contain exactly two blocks of `3`s, consistently following the first-block-to-1s, second-block-to-2s pattern.

**YAML Fact Document:**


```yaml
task_elements:
  - object: sequence
    description: A sequence of single-digit integers.
    properties:
      - type: list or array of integers
      - elements: 0, 3 (input); 0, 1, 2 (output)
      - length: preserved between input and output

  - object: number_0
    properties:
      - value: 0
      - role: separator, identity element
    action:
      - maps directly to 0 in the output at the same position.

  - object: number_3
    properties:
      - value: 3
      - role: element to be transformed
    action:
      - transformed based on block context and order.

  - object: block_of_3s
    description: A contiguous subsequence containing only the number 3.
    properties:
      - composed_of: number_3
      - separator: number_0
      - order_of_appearance: ordinal position (1st, 2nd, etc.) when scanning left-to-right.
    relationships:
      - blocks are distinct segments within the main sequence.
      - transformation depends on the block's order_of_appearance.
    action:
      - if order_of_appearance is 1, transform all 3s in the block to 1s.
      - if order_of_appearance is 2, transform all 3s in the block to 2s.

  - object: transformation_rule
    description: The overall process mapping input sequence to output sequence.
    properties:
      - preserves sequence length.
      - maps 0 to 0.
      - identifies contiguous blocks of 3s separated by 0s.
      - maps the first block of 3s to 1s.
      - maps the second block of 3s to 2s.
```


**Natural Language Program:**

1.  Initialize an empty output sequence and a counter for blocks of `3`s encountered (set to 0).
2.  Iterate through the input sequence from left to right.
3.  If the current element is `0`, append `0` to the output sequence.
4.  If the current element is `3`:
    a.  Check if this `3` starts a new block (i.e., it's the first `3` encountered, or the previous element was `0`).
    b.  If it starts a new block, increment the block counter.
    c.  Determine the target value based on the block counter: if the counter is 1, the target value is `1`; if the counter is 2, the target value is `2`.
    d.  Append the target value to the output sequence.
5.  Continue iterating until the end of the input sequence is reached.
6.  Return the constructed output sequence.
