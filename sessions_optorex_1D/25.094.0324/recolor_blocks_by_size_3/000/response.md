*   **Perception of Task Elements:**
    *   The input and output are sequences of integers of the same length (12 elements).
    *   Input sequences contain only the integers `0` and `3`.
    *   Output sequences contain the integers `0`, `1`, and `2`.
    *   The value `0` in the input sequence consistently maps to `0` in the output sequence at the same position.
    *   The value `3` in the input sequence maps to either `1` or `2` in the output sequence.
    *   The transformation of `3`s appears to depend on contiguous groups (runs) of `3`s within the input sequence.
    *   There seem to be two distinct groups of `3`s in each input example, separated by `0`s or the sequence boundaries.
    *   The length of these groups of `3`s determines whether they are transformed into `1`s or `2`s. Specifically, the longer group of `3`s becomes `1`s, and the shorter group becomes `2`s.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_sequence
        properties:
          - type: list_of_integers
          - allowed_values: [0, 3]
          - length: 12
      - object: output_sequence
        properties:
          - type: list_of_integers
          - allowed_values: [0, 1, 2]
          - length: 12
      - object: sequence_element
        properties:
          - value: integer
          - position: index
      - object: group_of_threes
        properties:
          - type: contiguous_subsequence
          - element_value: 3
          - length: integer
          - start_index: integer
          - end_index: integer
    relationships:
      - type: mapping
        from: input_sequence.element[i]
        to: output_sequence.element[i]
      - condition: input_sequence.element[i] == 0
        implies: output_sequence.element[i] == 0
      - condition: input_sequence.element[i] == 3
        implies: output_sequence.element[i] in [1, 2]
    actions:
      - action: identify_groups
        description: Find all contiguous subsequences consisting solely of the value 3 in the input sequence.
        inputs: input_sequence
        outputs: list_of_group_of_threes
      - action: compare_group_lengths
        description: Compare the lengths of the identified groups of threes. Assume there are exactly two groups.
        inputs: list_of_group_of_threes
        outputs: longer_group, shorter_group
      - action: transform_elements
        description: Create the output sequence based on the input sequence and group comparison.
        inputs: input_sequence, longer_group, shorter_group
        outputs: output_sequence
        steps:
          - Initialize output_sequence as a copy of input_sequence.
          - For elements corresponding to the longer_group in the input, set their value to 1 in the output_sequence.
          - For elements corresponding to the shorter_group in the input, set their value to 2 in the output_sequence.
          - Keep elements with value 0 unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as the input sequence.
    2.  Identify all distinct contiguous groups (runs) of the number `3` in the input sequence. Record the start index, end index, and length of each group. Assume there will be exactly two such groups.
    3.  Compare the lengths of the two identified groups of `3`s.
    4.  Determine which group is longer and which is shorter.
    5.  Iterate through the input sequence by index:
        a.  If the element at the current index is `0`, place `0` at the corresponding index in the output sequence.
        b.  If the element at the current index belongs to the *longer* group of `3`s (identified in step 3), place `1` at the corresponding index in the output sequence.
        c.  If the element at the current index belongs to the *shorter* group of `3`s (identified in step 3), place `2` at the corresponding index in the output sequence.
    6.  Return the generated output sequence.