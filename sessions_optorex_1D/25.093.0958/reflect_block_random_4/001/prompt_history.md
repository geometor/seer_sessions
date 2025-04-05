
## train_1

**input:**
```
0 0 0 0 9 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 8 9 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 2 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 2 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 3 5 9 3 5 2 4 0 0 0 0
```


**output:**
```
0 4 2 5 3 9 5 3 0 0 0 0
```


## train_4

**input:**
```
0 0 0 5 3 2 2 6 3 4 0 0
```


**output:**
```
0 0 0 4 3 6 2 2 3 5 0 0
```


## train_5

**input:**
```
0 0 0 0 0 3 5 1 4 0 0 0
```


**output:**
```
0 0 0 0 0 4 1 5 3 0 0 0
```


## train_6

**input:**
```
0 0 7 4 6 9 6 9 9 4 5 4
```


**output:**
```
0 0 4 5 4 9 9 6 9 6 4 7
```


## train_7

**input:**
```
0 0 0 0 0 0 1 4 9 1 5 3
```


**output:**
```
0 0 0 0 0 0 3 5 1 9 4 1
```

**Perception of Task Elements:**

The task involves manipulating sequences of single-digit integers. Each input sequence is transformed into an output sequence of the same length. The key observation is the role of the zero ('0') elements versus the non-zero elements. The zeros appear to act as padding or boundaries, while the core transformation happens on the contiguous block of non-zero numbers (and any zeros interspersed *within* that block). Specifically, the segment of the sequence starting from the first non-zero digit and ending with the last non-zero digit is reversed. The zeros outside this segment (leading and trailing zeros) remain unchanged in their positions.

**Facts:**


```yaml
objects:
  - type: sequence
    description: A list of single-digit integers (0-9).
    properties:
      - length: The number of integers in the sequence.
      - elements: The individual integers in the sequence.
      - contains_zeros: Boolean indicating if the sequence includes the digit 0.
      - contains_non_zeros: Boolean indicating if the sequence includes digits 1-9.
  - type: sub-sequence
    description: A contiguous portion of the main sequence.
    properties:
      - start_index: The index of the first element of the sub-sequence in the main sequence.
      - end_index: The index of the last element of the sub-sequence in the main sequence.
      - elements: The integers within the sub-sequence.

actions:
  - name: identify_non_zero_segment
    description: Find the portion of the sequence from the first non-zero element to the last non-zero element.
    inputs:
      - sequence: The input sequence.
    outputs:
      - start_index: Index of the first non-zero element (or None if all zeros).
      - end_index: Index of the last non-zero element (or None if all zeros).
  - name: extract_sub_sequence
    description: Get the elements within a specified range of indices.
    inputs:
      - sequence: The main sequence.
      - start_index: The starting index (inclusive).
      - end_index: The ending index (inclusive).
    outputs:
      - sub_sequence: The extracted sequence of elements.
  - name: reverse_sequence
    description: Reverse the order of elements in a sequence.
    inputs:
      - sequence: The sequence to be reversed.
    outputs:
      - reversed_sequence: The sequence with elements in reverse order.
  - name: construct_output
    description: Build the final output sequence by replacing the identified segment with its reversed version.
    inputs:
      - original_sequence: The input sequence.
      - start_index: The start index of the segment that was reversed.
      - end_index: The end index of the segment that was reversed.
      - reversed_sub_sequence: The reversed segment.
    outputs:
      - output_sequence: The final transformed sequence.

relationships:
  - The output sequence has the same length as the input sequence.
  - Elements outside the segment defined by the first and last non-zero numbers remain in their original positions.
  - The segment from the first non-zero number to the last non-zero number in the input corresponds to the reversed version of that same segment in the output.
  - If the input sequence contains no non-zero numbers, the output sequence is identical to the input sequence.
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Determine the index of the first non-zero digit and the index of the last non-zero digit in the input sequence.
3.  If no non-zero digits are found, return the original input sequence.
4.  Extract the sub-sequence starting from the index of the first non-zero digit up to and including the index of the last non-zero digit.
5.  Reverse the order of the elements within this extracted sub-sequence.
6.  Create the output sequence by concatenating:
    a.  The elements from the beginning of the input sequence up to (but not including) the index of the first non-zero digit.
    b.  The reversed sub-sequence.
    c.  The elements from the input sequence starting from the position immediately after the index of the last non-zero digit until the end of the sequence.
7.  Return the constructed output sequence.
