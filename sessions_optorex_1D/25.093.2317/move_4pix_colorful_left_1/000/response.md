Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are strings representing sequences of single digits separated by spaces. They can be interpreted as lists or arrays of integers.
2.  **Sequence Length:** The length of the sequence remains constant between the input and the output in all examples.
3.  **Core Content:** The non-zero digits and the zeros situated between the first and last non-zero digits seem to form a "core segment" or "payload". This core segment appears unchanged in the output.
4.  **Positional Shift:** The primary transformation is a positional shift of this core segment within the sequence. The core segment consistently moves towards the beginning of the sequence (left shift).
5.  **Shift Magnitude:** The amount of the left shift appears deterministic. By comparing the number of leading zeros in the input versus the output, we can deduce the rule.
    *   train_1: 8 leading zeros in -> 4 leading zeros out (Shift of 4 positions left)
    *   train_2: 4 leading zeros in -> 0 leading zeros out (Shift of 4 positions left)
    *   train_3: 5 leading zeros in -> 1 leading zero out (Shift of 4 positions left)
    *   train_4: 4 leading zeros in -> 0 leading zeros out (Shift of 4 positions left)
    *   train_5: 6 leading zeros in -> 2 leading zeros out (Shift of 4 positions left)
    *   train_6: 6 leading zeros in -> 2 leading zeros out (Shift of 4 positions left)
    *   train_7: 5 leading zeros in -> 1 leading zero out (Shift of 4 positions left)
    The number of leading zeros in the output is consistently 4 less than the number of leading zeros in the input, with a minimum of 0 leading zeros.

**YAML Fact Document:**


```yaml
task_description: Rearrange a sequence of digits by shifting the core non-zero segment to the left.
elements:
  - object: sequence
    properties:
      - type: list of integers (derived from space-separated string)
      - length: constant between input and output
      - items: single digits (0-9)
  - object: core_segment
    description: The subsequence starting from the first non-zero digit and ending at the last non-zero digit, inclusive.
    properties:
      - content: digits (non-zero and potentially included zeros)
      - location_input: defined by the index of the first non-zero digit (number of leading zeros)
      - location_output: derived from the input location
relationships:
  - type: transformation
    action: identify_core_segment
    inputs: [input_sequence]
    outputs: [core_segment, first_nonzero_index, last_nonzero_index]
  - type: transformation
    action: calculate_output_position
    inputs: [first_nonzero_index]
    outputs: [output_leading_zeros]
    rule: output_leading_zeros = max(0, first_nonzero_index - 4)
  - type: transformation
    action: reconstruct_output
    inputs: [output_leading_zeros, core_segment, input_sequence_length]
    outputs: [output_sequence]
    rule: Concatenate 'output_leading_zeros' count of zeros, the 'core_segment', and trailing zeros to match 'input_sequence_length'.
special_cases:
  - condition: Input sequence contains only zeros.
    result: Output sequence is identical to the input sequence. (The core segment is empty, leading zeros calculation still applies but doesn't change the sequence visually).
```


**Natural Language Program:**

1.  Parse the input string into a list of integers. Record the total length of this list.
2.  Locate the index of the first non-zero integer in the list (`first_nz_idx`). If no non-zero integer exists, return the original input string.
3.  Locate the index of the last non-zero integer in the list (`last_nz_idx`).
4.  Extract the sub-list from `first_nz_idx` to `last_nz_idx` (inclusive). This is the "core segment".
5.  Calculate the number of leading zeros for the output list: `num_output_zeros = max(0, first_nz_idx - 4)`.
6.  Construct the output list:
    a.  Start with `num_output_zeros` zeros.
    b.  Append the extracted "core segment" to the list.
    c.  Append additional zeros until the total length of the output list matches the recorded length of the input list.
7.  Convert the output list back into a space-separated string of digits.