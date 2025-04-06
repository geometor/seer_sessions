
## train_1

**input:**
```
0 7 0
0 0 0
0 0 0
```


**output:**
```
7
```


## train_2

**input:**
```
0 2 0
2 0 0
0 2 0
```


**output:**
```
2 2 2
```


## train_3

**input:**
```
0 8 0
8 8 0
8 0 0
```


**output:**
```
8 8 8 8
```


## train_4

**input:**
```
0 0 0
1 0 0
0 1 0
```


**output:**
```
1 1
```

**Perception of Task Elements:**

The task involves processing a 2-dimensional grid of numbers (specifically 3x3 grids in the examples). The core operation is extracting specific values from this grid and arranging them into a linear sequence. The defining characteristic of the extracted values is that they are non-zero. The order in the output sequence corresponds to the standard reading order (left-to-right, top-to-bottom) of the input grid.

**YAML Facts:**


```yaml
Input:
  type: grid
  dimensionality: 2
  data_type: integer
  properties:
    - contains zeros and non-zero numbers
    - fixed size (3x3 in examples, might be general)
Output:
  type: sequence
  dimensionality: 1
  data_type: integer
  properties:
    - contains only the non-zero numbers from the input
    - order matches the reading order of non-zero elements in the input grid
Transformation:
  action: extraction
  rule: collect non-zero elements
  order: row-major (top-to-bottom, left-to-right)
Relationships:
  - The output sequence length equals the count of non-zero elements in the input grid.
  - Each element in the output sequence is identical to a non-zero element in the input grid.
  - The position of an element in the output sequence is determined by its position in the input grid relative to other non-zero elements when scanned in reading order.
```


**Natural Language Program:**

1.  Iterate through the rows of the input grid from top to bottom.
2.  For each row, iterate through its elements from left to right.
3.  If an element is not zero, add it to a new list.
4.  Concatenate the elements in the new list into a single output sequence, maintaining their order of addition.
