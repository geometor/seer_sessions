
## train_1

**input:**
```
2 4 1 0 5 5 0 5 5 0 5 5
```


**output:**
```
2 4 1 0 2 2 0 4 4 0 1 1
```


## train_2

**input:**
```
3 2 0 0 0 5 5 0 0 5 5 0
```


**output:**
```
3 2 0 0 0 3 3 0 0 2 2 0
```


## train_3

**input:**
```
6 5 9 5 5 0 5 5 0 0 5 5
```


**output:**
```
6 5 9 6 6 0 5 5 0 0 9 9
```


## train_4

**input:**
```
5 0 0 0 0 0 5 5 5 5 0 0
```


**output:**
```
5 0 0 0 0 0 5 5 5 5 0 0
```


## train_5

**input:**
```
6 0 0 0 0 0 0 0 5 5 5 0
```


**output:**
```
6 0 0 0 0 0 0 0 6 6 6 0
```


## train_6

**input:**
```
2 0 0 0 0 5 5 5 5 0 0 0
```


**output:**
```
2 0 0 0 0 2 2 2 2 0 0 0
```


## train_7

**input:**
```
4 1 0 0 5 5 0 0 5 5 0 0
```


**output:**
```
4 1 0 0 4 4 0 0 1 1 0 0
```

*   **Perception of Elements:**
    *   The input and output are sequences of single-digit integers.
    *   The length of the sequence remains constant (12 digits in the examples).
    *   The digit '0' appears to act as a separator or boundary and remains unchanged in the output.
    *   The digit '5' in the input is the primary target for transformation. Occurrences of '5' are replaced by other digits.
    *   Other non-zero digits (besides '5') seem to serve as "source" values for the replacement.
    *   Consecutive sequences (blocks) of '5's in the input are replaced entirely by repeating a single digit from the source values.
    *   The source values used for replacement appear to be the non-zero digits from the input, excluding the '5's that are part of the replaceable blocks, taken in the order they appear.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - item: input_sequence
        properties:
          - type: list of integers
          - length: 12 (in examples)
          - contains: digits 0-9
      - item: output_sequence
        properties:
          - type: list of integers
          - length: same as input
          - derived_from: input_sequence
      - item: key_digit_value
        value: 5
        role: placeholder for replacement
      - item: separator_digit_value
        value: 0
        role: boundary, unchanged
      - item: source_digits
        derivation: sequence of non-zero digits in the input, excluding instances of the key_digit_value (5) that are part of contiguous blocks to be replaced.
        order: preserved from input
      - item: key_digit_blocks
        derivation: contiguous sequences of the key_digit_value (5) in the input.
        relationship: each block corresponds sequentially to one source_digit.
    transformation:
      action: replace
      target: each key_digit_block in the input
      rule: replace every digit within a block with the corresponding source_digit based on the block's order of appearance.
      unchanged_elements: digits that are not the key_digit_value (5) and the separator_digit_value (0).
    ```


*   **Natural Language Program:**
    1.  Identify all non-zero digits in the input sequence that are *not* the digit '5'. Store these identified digits in a list, preserving their original order. Call this the "source list".
    2.  Initialize an index variable, `source_index`, to 0.
    3.  Create a new empty list to store the output sequence.
    4.  Iterate through the input sequence digit by digit.
    5.  If the current digit is '5':
        *   Append the digit from the "source list" at the current `source_index` to the output sequence.
        *   Check if the next digit in the input sequence is *not* '5'. If it is not '5' (or if it's the end of the sequence), increment the `source_index` by 1 (to move to the next source digit for the next block of '5's).
    6.  If the current digit is *not* '5':
        *   Append the current digit directly to the output sequence.
    7.  Return the completed output sequence.
