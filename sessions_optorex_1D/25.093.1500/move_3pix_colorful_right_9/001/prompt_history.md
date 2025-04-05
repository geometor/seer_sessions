
## train_1

**input:**
```
0 0 0 0 7 5 5 9 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 5 5 9 8
```


## train_2

**input:**
```
0 0 0 0 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 0 0 0 0
```


## train_3

**input:**
```
0 2 4 9 3 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 4 9 3 7 0 0 0
```


## train_4

**input:**
```
2 4 9 8 8 7 9 0 0 0 0 0
```


**output:**
```
0 0 0 2 4 9 8 8 7 9 0 0
```


## train_5

**input:**
```
0 0 0 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 0 0 0 0 0
```


## train_6

**input:**
```
0 0 4 6 2 5 6 4 3 0 0 0
```


**output:**
```
0 0 0 0 0 4 6 2 5 6 4 3
```


## train_7

**input:**
```
0 9 1 8 6 4 5 8 5 0 0 0
```


**output:**
```
0 0 0 0 9 1 8 6 4 5 8 5
```

**Perception of Task Elements:**

The task involves manipulating a sequence of single-digit integers. The core operation appears to be spatial rearrangement based on the values within the sequence. Specifically, non-zero elements are treated as a cohesive block that is shifted within the sequence.

1.  **Input/Output Format:** Both input and output are lists (or sequences) of single-digit integers, separated by spaces. The length of the sequence remains constant between input and output (12 elements in all examples).
2.  **Key Objects:** The primary objects are the individual integers in the sequence. We can distinguish between zero and non-zero integers. A significant composite object is the contiguous block of non-zero integers.
3.  **Transformation:** The transformation identifies the block of consecutive non-zero integers (if any exist) and shifts this entire block 3 positions to the right. The positions vacated by the shift and the positions originally occupied by the start of the shifted block become zeros. If the input consists entirely of zeros, the output remains unchanged.

**YAML Facts:**


```yaml
task_elements:
  - item: input_sequence
    type: List[int]
    properties:
      - length: fixed (e.g., 12)
      - elements: single digits (0-9)
  - item: output_sequence
    type: List[int]
    properties:
      - length: same as input_sequence
      - elements: single digits (0-9)
  - item: non_zero_block
    type: List[int]
    description: A contiguous sub-sequence of the input_sequence containing only non-zero integers, bounded by zeros or the sequence ends.
    properties:
      - start_index: The index of the first element of the block in the input_sequence.
      - end_index: The index of the last element of the block in the input_sequence.
      - elements: The non-zero integers forming the block.
relationships:
  - type: positional_shift
    source: non_zero_block (from input_sequence)
    target: non_zero_block (in output_sequence)
    details: The starting index of the non_zero_block in the output_sequence is exactly 3 greater than its starting index in the input_sequence.
  - type: element_replacement
    details: All positions in the output_sequence are initially zero. The non_zero_block from the input is then placed into the output_sequence at the calculated shifted position.
actions:
  - action: identify_non_zero_block
    input: input_sequence
    output: non_zero_block, start_index, end_index
    description: Find the first and last indices bounding the contiguous sequence of non-zero numbers. Extract this sequence. Handle the case where no non-zero numbers exist.
  - action: construct_output
    input: input_sequence_length, non_zero_block, start_index
    output: output_sequence
    description: Create a new sequence of zeros with the same length as the input. Place the non_zero_block into this new sequence starting at index (start_index + 3). If no non_zero_block was found, the output is the sequence of zeros.
```


**Natural Language Program:**

1.  Receive the input sequence of numbers.
2.  Initialize an output sequence of the same length, filled entirely with zeros.
3.  Scan the input sequence to find the index of the first non-zero number (`start_index`) and the index of the last non-zero number (`end_index`).
4.  If no non-zero numbers are found in the input sequence, the process is complete, and the initialized output sequence (all zeros) is the result.
5.  If non-zero numbers are found, extract the sub-sequence from `start_index` to `end_index` (inclusive) from the input sequence. This is the `non_zero_block`.
6.  Calculate the target starting position for the block in the output sequence by adding 3 to the `start_index`.
7.  Place the extracted `non_zero_block` into the output sequence, starting at the calculated target position.
8.  Return the final output sequence.
