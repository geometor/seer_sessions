Okay, let's analyze the input-output pairs.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists) of 12 single digits, represented as space-separated numbers.
2.  **Structure:** Each sequence seems to have two parts:
    *   A fixed prefix: The first four digits are always `0 0 0 0`.
    *   A variable suffix: The remaining eight digits (indices 4 to 11) vary between examples.
3.  **Content of Suffix:** The suffix consists primarily of one specific non-zero digit (let's call it `X`) and the digit `0`. In all examples, the suffix contains exactly six instances of `X` and two instances of `0`.
4.  **Transformation:** The transformation only affects the suffix (the last eight digits). The prefix `0 0 0 0` remains unchanged.
5.  **Rule Identification:** By comparing the input and output suffixes, a pattern emerges. When the input suffix does *not* match the pattern `X X X 0 X X 0 X`, it is rearranged to fit this pattern in the output. If the input suffix *already* matches this pattern, the output is identical to the input.

**YAML Facts:**


```yaml
task_elements:
  - object: sequence
    type: list_of_integers
    properties:
      length: 12
  - object: prefix
    part_of: sequence
    indices: 0-3
    properties:
      value: [0, 0, 0, 0]
      constant: true
  - object: suffix
    part_of: sequence
    indices: 4-11
    properties:
      length: 8
      variable: true
      composition:
        - type: non_zero_digit (X)
          count: 6
        - type: zero_digit (0)
          count: 2
  - object: target_pattern
    description: The desired arrangement for the suffix.
    value_template: [X, X, X, 0, X, X, 0, X] # Where X is the non-zero digit
    applies_to: suffix

actions:
  - name: identify_non_zero_digit
    input: suffix
    output: digit_X
    description: Find the unique non-zero digit present in the suffix.
  - name: check_suffix_pattern
    input: suffix
    comparison: target_pattern
    output: boolean (matches or not)
    description: Check if the input suffix matches the target pattern `X X X 0 X X 0 X`.
  - name: rearrange_suffix
    input: suffix
    output: rearranged_suffix (matching target_pattern)
    description: Reorder the elements (six X's and two 0's) in the suffix to match the target pattern `X X X 0 X X 0 X`.
  - name: construct_output
    inputs: [prefix, rearranged_suffix (or original suffix if it matched)]
    output: output_sequence
    description: Combine the original prefix with the potentially rearranged suffix.

relationships:
  - type: composition
    subject: sequence
    objects: [prefix, suffix]
  - type: transformation_condition
    condition: "input suffix does not match target_pattern"
    action: rearrange_suffix
  - type: transformation_condition
    condition: "input suffix matches target_pattern"
    action: keep_suffix_unchanged

```


**Natural Language Program:**

1.  Examine the input sequence of 12 digits.
2.  Identify the prefix (first four digits) and the suffix (last eight digits).
3.  Verify that the prefix is `0 0 0 0`.
4.  Examine the suffix (indices 4 to 11). Identify the unique non-zero digit present, let's call it `X`. Confirm there are six instances of `X` and two instances of `0`.
5.  Define the target pattern for the suffix as `X X X 0 X X 0 X`.
6.  Check if the input suffix matches the target pattern.
7.  If the input suffix matches the target pattern, the output sequence is identical to the input sequence.
8.  If the input suffix does *not* match the target pattern, construct the output sequence by keeping the original prefix (`0 0 0 0`) and appending a new suffix rearranged into the target pattern (`X X X 0 X X 0 X` using the six `X`s and two `0`s from the input suffix).