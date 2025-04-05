
## train_1

**input:**
```
0 0 4 4 7 7 9 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 4 7 7 9 7
```


## train_2

**input:**
```
0 1 6 4 8 2 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 6 4 8 2 0 0
```


## train_3

**input:**
```
0 0 0 0 3 6 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 6 8 0
```


## train_4

**input:**
```
0 0 0 0 0 2 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 9 0
```


## train_5

**input:**
```
2 7 1 9 9 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 7 1 9 9 5 5 0
```


## train_6

**input:**
```
0 0 0 0 3 1 9 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 1 9 0
```


## train_7

**input:**
```
1 3 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 3 4 0 0 0 0 0
```

*   **Perception:** The task involves processing fixed-length sequences of 12 digits. Each input sequence appears to contain a contiguous block defined by the first and last non-zero digits. This block (including any zeros it might contain internally) is shifted 4 positions to the right within the 12-digit frame to produce the output. The positions outside the shifted block in the output are filled with zeros.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - item: input_sequence
        properties:
          - type: list of integers
          - length: 12
          - content: digits (0-9) separated by spaces in string format
      - item: output_sequence
        properties:
          - type: list of integers
          - length: 12
          - content: digits (0-9) separated by spaces in string format
      - item: non_zero_segment
        properties:
          - definition: The sub-sequence starting from the first non-zero digit and ending with the last non-zero digit in the input sequence.
          - may_contain_zeros: true
      - item: shift_operation
        properties:
          - type: right shift
          - amount: 4 positions
          - target: non_zero_segment
      - item: zero_padding
        properties:
          - description: Positions in the output sequence not occupied by the shifted segment are filled with zeros.
          - handling_boundaries: Elements shifted beyond the 12th position are truncated/discarded.
    relationships:
      - input_sequence is transformed into output_sequence by identifying the non_zero_segment, applying the shift_operation, and using zero_padding.
      - If input_sequence contains only zeros, the non_zero_segment is empty, and the output_sequence is identical to the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 integers.
    2.  Identify the index of the first non-zero element (`first_nz`) and the index of the last non-zero element (`last_nz`) in the input list.
    3.  If no non-zero elements are found (i.e., the list contains only zeros), return the original input string.
    4.  Extract the sub-list (segment) from the input list starting at index `first_nz` and ending at index `last_nz` (inclusive).
    5.  Create a new list of 12 zeros, representing the initial state of the output list.
    6.  Calculate the starting index for placing the extracted segment in the output list: `target_start = first_nz + 4`.
    7.  Iterate through the extracted segment. For each element in the segment, calculate its target index in the output list by adding its position relative to the start of the segment to `target_start`.
    8.  If the calculated target index is within the bounds of the output list (0 to 11), place the element at that index in the output list. Otherwise, discard the element (truncation).
    9.  Convert the resulting output list back into a space-separated string of digits.
    10. Return the formatted output string.
