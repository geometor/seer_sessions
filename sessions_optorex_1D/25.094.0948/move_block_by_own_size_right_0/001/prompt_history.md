
## train_1

**input:**
```
0 0 0 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 0 0
```


## train_4

**input:**
```
0 0 5 5 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 5
```


## train_6

**input:**
```
4 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```


## train_7

**input:**
```
5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 5 5 5 5
```

## Perception of Task Elements

The input and output are both sequences (or lists) of 12 integers.
Each input sequence contains a single contiguous block of identical non-zero integers, surrounded by zeros. The zeros act as padding or empty space.
The transformation involves moving this block of non-zero integers within the sequence.
The direction of movement is always to the right.
The distance the block moves appears to be directly related to the number of elements in the block (its length).

## Facts


```yaml
Input:
  type: list
  element_type: integer
  length: 12
  contains:
    - zeros: representing empty space
    - object:
        type: contiguous block
        properties:
          value: non-zero integer (consistent within the block)
          length: variable (number of elements in the block)
          start_index: position of the first element of the block
          end_index: position of the last element of the block
Output:
  type: list
  element_type: integer
  length: 12
  structure: derived from input by applying a transformation
Transformation:
  action: shift_right
  target: object (the contiguous block of non-zero integers)
  parameter: shift_distance
  relationship: shift_distance equals the length of the object
  effect:
    - The object moves to a new position.
    - The new start_index = old start_index + shift_distance.
    - The original positions occupied by the object become zeros.
Constraints:
  - The sequence length remains 12.
  - There is only one contiguous block of non-zero numbers in the input.
  - The shift operation occurs within the bounds of the sequence (no wrap-around or truncation observed in examples).
```


## Natural Language Program

1.  **Identify the Object:** Scan the input sequence to find the contiguous block of identical non-zero integers. Note its value, its starting index, and its length (number of elements).
2.  **Calculate Shift Distance:** Determine the shift distance, which is equal to the length of the identified block.
3.  **Create Output Sequence:** Initialize a new sequence of 12 zeros.
4.  **Place Shifted Object:** Calculate the new starting index for the block by adding the shift distance to the original starting index. Copy the identified block of non-zero integers into the new sequence starting at this new calculated index.
5.  **Return Output:** The resulting sequence is the output.
