
## train_1

**input:**
```
0 3 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 4 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 4 1 1 2 6 0 0 0 0
```


**output:**
```
0 0 0 0 4 1 1 2 6 0 0 0
```


## train_3

**input:**
```
8 1 2 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 1 2 1 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 5 9 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 5 9 6 0 0
```


## train_5

**input:**
```
0 2 5 2 8 7 1 7 9 6 1 0
```


**output:**
```
0 0 2 5 2 8 7 1 7 9 6 1
```


## train_6

**input:**
```
0 0 0 4 2 6 8 4 5 7 0 0
```


**output:**
```
0 0 0 0 4 2 6 8 4 5 7 0
```


## train_7

**input:**
```
0 0 0 0 0 5 5 9 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 9 0 0 0
```

## Perception

The input and output are sequences (lists) of single-digit integers, always of the same length (12 in the examples). The transformation involves shifting a specific sub-sequence within the list one position to the right.

1.  **Identify Key Elements:** The core elements are the sequence itself and a sub-sequence within it. This sub-sequence appears to be defined by the positions of the first and last non-zero numbers. Zeros within this sub-sequence are treated as part of the sub-sequence.
2.  **Identify the Action:** The primary action is a 'shift right' operation applied to the identified sub-sequence.
3.  **Identify Invariants:** The length of the sequence remains constant. The relative order and values of the elements *within* the shifted sub-sequence are preserved. Elements *before* the sub-sequence also remain in their original positions.
4.  **Identify Changes:** The sub-sequence moves one position to the right. The position immediately preceding the original start of the sub-sequence becomes 0. Elements originally after the sub-sequence might be overwritten or effectively dropped if the shift extends to the end of the list's bounds.

## Facts


```yaml
task_elements:
  - item: sequence
    type: list
    subtype: integer
    properties:
      - length: fixed (e.g., 12 in examples)
      - elements: single digits (0-9)
  - item: active_subsequence
    type: sublist
    derivation: determined by the span from the first non-zero element to the last non-zero element in the input sequence.
    properties:
      - includes all elements within its start and end indices, including any zeros.
      - If the input sequence contains only zeros, this subsequence is considered empty or non-existent.
relationships:
  - input sequence contains the active_subsequence.
  - output sequence is derived from the input sequence.
actions:
  - identify: find the start and end indices of the active_subsequence in the input.
  - shift: move the active_subsequence one position to the right.
  - insert: place a zero at the original starting position of the active_subsequence.
  - preserve: maintain the original elements located before the active_subsequence.
  - maintain_length: ensure the output sequence has the same length as the input sequence (elements shifted beyond the original boundary are implicitly dropped).
transformation:
  - condition: If an active_subsequence exists (i.e., at least one non-zero element is present).
    steps:
      - Locate the index of the first non-zero element (`start_index`).
      - Locate the index of the last non-zero element (`end_index`).
      - Construct the output sequence by:
        - Copying elements from index 0 to `start_index - 1` from the input to the output at the same indices.
        - Placing a 0 at `start_index` in the output.
        - Copying elements from `start_index` to `end_index` from the input to the output, starting at index `start_index + 1` and ending at `end_index + 1`.
        - Filling any remaining positions in the output (after `end_index + 1`) with zeros, up to the original sequence length.
  - condition: If no active_subsequence exists (input is all zeros).
    steps:
      - The output sequence is identical to the input sequence.

```


## Natural Language Program

1.  Examine the input sequence of numbers.
2.  Find the index of the first non-zero number (`first_nz`).
3.  Find the index of the last non-zero number (`last_nz`).
4.  If no non-zero numbers are found (the sequence is all zeros), the output is identical to the input.
5.  Otherwise:
    a.  Create a new output sequence of the same length as the input, initially filled with zeros.
    b.  Copy the elements from the input sequence from index 0 up to (but not including) `first_nz` into the output sequence at the same positions.
    c.  Copy the elements from the input sequence starting at index `first_nz` up to and including index `last_nz` into the output sequence, starting at index `first_nz + 1` and ending at index `last_nz + 1`.
6.  Return the newly constructed output sequence.
