
## train_1

**input:**
```
0 0 0 0 0 4 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 6 0 0 0 0 0 6 0 0 0 0
```


## train_3

**input:**
```
0 0 7 7 7 7 7 7 7 7 7 0
```


**output:**
```
0 0 7 0 0 0 0 0 0 0 7 0
```


## train_4

**input:**
```
0 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 5 0 0 0 0 0 0
```


## train_5

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
1 0 0 0 0 0 0 0 0 0 0 1
```


## train_6

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
0 1 0 0 0 0 0 0 0 0 0 1
```


## train_7

**input:**
```
0 0 3 3 3 3 0 0 0 0 0 0
```


**output:**
```
0 0 3 0 0 3 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task involves processing a sequence of single-digit integers. The core operation focuses on identifying contiguous blocks (or subsequences) of identical non-zero numbers within the input sequence. The transformation rule depends on the length of these blocks. Zeros in the input sequence generally remain unchanged unless they are part of the modification applied to a non-zero block. The output sequence always has the same length as the input sequence.

**YAML Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    description: Represents both the input and output data structures.
  - name: non_zero_block
    type: subsequence
    description: A contiguous run of identical non-zero integers within the input sequence.
properties:
  - object: sequence
    name: length
    type: integer
    description: The number of elements in the sequence.
  - object: non_zero_block
    name: value
    type: integer
    description: The non-zero integer value repeated in the block.
  - object: non_zero_block
    name: start_index
    type: integer
    description: The index of the first element of the block in the original sequence.
  - object: non_zero_block
    name: end_index
    type: integer
    description: The index of the last element of the block in the original sequence.
  - object: non_zero_block
    name: block_length
    type: integer
    description: The number of elements in the block (calculated as end_index - start_index + 1).
actions:
  - name: identify_blocks
    description: Scan the input sequence to find all non_zero_blocks.
  - name: hollow_out_block
    description: Modify a block in the output sequence by setting its interior elements (all except the first and last) to zero.
relationships:
  - The output sequence is generated from the input sequence.
  - The transformation is applied based on the properties (specifically block_length) of identified non_zero_blocks.
  - If a non_zero_block has a block_length greater than 2, the hollow_out_block action is applied to the corresponding positions in the output sequence.
  - If a non_zero_block has a block_length of 1 or 2, it remains unchanged in the output sequence.
  - Elements originally zero remain zero unless they fall within the indices being modified by the hollow_out_block action.
```


**Natural Language Program:**

1.  Start with the input sequence.
2.  Create a mutable copy of the input sequence; this will become the output sequence.
3.  Iterate through the input sequence to identify all contiguous subsequences (blocks) consisting of the same non-zero number. Keep track of the start index, end index, and the non-zero value for each block.
4.  For each identified non-zero block:
    a.  Calculate the length of the block.
    b.  If the length of the block is greater than 2:
        i.  In the output sequence, iterate from the index immediately *after* the block's start index up to the index *before* the block's end index.
        ii. Set the value of each element at these indices to 0.
5.  Return the modified output sequence.
