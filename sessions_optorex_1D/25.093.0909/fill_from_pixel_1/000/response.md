Okay, let's break down the transformation logic based on the provided examples.

**Perception of Task Elements:**

The task involves manipulating sequences of 12 single-digit integers. The core operation seems to be propagating a non-zero digit into adjacent blocks of zeros at either the beginning or the end of the sequence. The key elements are:

1.  **Input Sequence:** A list of 12 integers.
2.  **Output Sequence:** A modified list of 12 integers.
3.  **Zero Blocks:** Contiguous sequences of zeros at the start (leading zeros) and end (trailing zeros) of the input sequence.
4.  **Non-Zero Boundaries:** The first non-zero digit encountered when reading from left to right, and the last non-zero digit encountered.
5.  **Propagation Rule:** A decision mechanism determines whether the first non-zero digit propagates leftwards into the leading zeros, or the last non-zero digit propagates rightwards into the trailing zeros. This decision appears to depend on the relative lengths of the leading and trailing zero blocks.

**Facts:**


```yaml
task_elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
      - contains: digits (0-9)
  - object: leading_zeros
    properties:
      - location: start of the sequence
      - value: 0
      - count: number of zeros before the first non-zero digit
  - object: trailing_zeros
    properties:
      - location: end of the sequence
      - value: 0
      - count: number of zeros after the last non-zero digit
  - object: first_non_zero
    properties:
      - value: the digit value of the first non-zero element
      - index: the position of the first non-zero element
  - object: last_non_zero
    properties:
      - value: the digit value of the last non-zero element
      - index: the position of the last non-zero element
relationships:
  - type: comparison
    between: count of leading_zeros
    and: count of trailing_zeros
actions:
  - action: identify_boundaries
    inputs: sequence
    outputs:
      - first_non_zero (value and index)
      - last_non_zero (value and index)
      - count of leading_zeros
      - count of trailing_zeros
  - action: conditional_fill
    condition: count of leading_zeros <= count of trailing_zeros
    operation_if_true: left_fill
    operation_if_false: right_fill
  - action: left_fill
    description: Replace all leading zeros in the sequence with the value of the first_non_zero digit.
    modifies: sequence (leading_zeros part)
  - action: right_fill
    description: Replace all trailing zeros in the sequence with the value of the last_non_zero digit.
    modifies: sequence (trailing_zeros part)

```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Identify the first non-zero digit (FNZ) and its index (`idx_fnz`). If no non-zero digit exists, return the input sequence unchanged.
3.  Identify the last non-zero digit (LNZ) and its index (`idx_lnz`).
4.  Count the number of leading zeros (`num_left_zeros`), which is equal to `idx_fnz`.
5.  Count the number of trailing zeros (`num_right_zeros`), which is equal to `11 - idx_lnz`.
6.  Compare `num_left_zeros` and `num_right_zeros`.
7.  If `num_left_zeros` is less than or equal to `num_right_zeros`, modify the sequence by replacing all digits from index 0 up to (but not including) `idx_fnz` with the value of FNZ.
8.  Otherwise (if `num_left_zeros` is greater than `num_right_zeros`), modify the sequence by replacing all digits from index `idx_lnz + 1` up to index 11 with the value of LNZ.
9.  Return the modified sequence.