
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 0 0 0
```


**output:**
```
0 2 0 0 0 0 0 0 2 0 0 0
```


## train_2

**input:**
```
0 3 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 3 0 0 0 0 0 0 0 3 0 0
```


## train_3

**input:**
```
0 0 0 0 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 3 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 9 9 9 9 9 0 0
```


**output:**
```
0 0 0 0 0 9 0 0 0 9 0 0
```


## train_5

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 0
```


**output:**
```
3 0 0 0 0 0 0 0 0 0 3 0
```


## train_6

**input:**
```
0 0 0 0 0 0 4 4 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 0 4 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 9 9 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 9 9 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of single-digit integers.
    *   The sequences have a fixed length (12 in all examples).
    *   The core elements within the sequences are contiguous blocks of identical non-zero numbers.
    *   Zeros act as separators or padding around these blocks.
    *   The transformation modifies these blocks of non-zero numbers, while leaving the original zeros unchanged.
    *   Specifically, within each block of identical non-zero numbers, only the first and the last occurrence are preserved in their original positions in the output sequence. All other numbers within that block (the ones between the first and last) are changed to zero.
    *   If a block consists of only one or two numbers, all numbers in that block are preserved as there are no numbers *between* the first and last.

*   **YAML Facts:**
    
```yaml
    task_type: sequence_transformation
    input_element_type: integer
    output_element_type: integer
    sequence_length: fixed (12 in examples)
    objects:
      - sequence: a list of integers.
      - block: a contiguous sub-sequence of identical non-zero integers within the main sequence.
      - zero: the integer 0, often acting as a boundary or filler.
    properties:
      - block:
          - value: the non-zero integer comprising the block.
          - start_index: the index of the first element of the block.
          - end_index: the index of the last element of the block.
          - length: the number of elements in the block (end_index - start_index + 1).
    relationships:
      - Blocks are separated by zeros or sequence boundaries.
      - The output sequence is derived from the input sequence.
    actions:
      - identify_blocks: Find all contiguous blocks of identical non-zero numbers in the input sequence.
      - preserve_boundaries: For each identified block, keep the number at the start_index and the number at the end_index in the output sequence.
      - zero_out_middle: For each identified block with length > 2, change the elements between the start_index and end_index to zero in the output sequence.
      - preserve_zeros: Keep all original zeros from the input sequence in the output sequence.
    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as a copy of the input sequence.
    2.  Iterate through the input sequence to identify contiguous blocks of identical non-zero numbers. Keep track of the start index, end index, and value for each block.
    3.  For each identified block:
        a.  If the block length is greater than 2 (i.e., the end index is more than one position after the start index):
            i.  Iterate from the index immediately after the start index up to (but not including) the end index.
            ii. Set the value at each of these intermediate indices in the *output* sequence to 0.
    4.  Return the modified output sequence. (Note: Zeros and blocks of length 1 or 2 are implicitly handled correctly by initializing the output as a copy and only modifying the middle of blocks longer than 2).
