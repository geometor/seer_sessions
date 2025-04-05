*   **Perception of Elements:**
    *   The input and output are sequences (strings) of space-separated single digits.
    *   Both input and output sequences have a fixed length (12 digits in the examples).
    *   The core elements are the individual digits within the sequence.
    *   Digits can be categorized into 'zero' and 'non-zero'.
    *   The transformation involves rearranging the digits based on whether they are zero or non-zero.

*   **YAML Facts:**
    
```yaml
    task_description: "Rearrange digits in a sequence, moving all zeros to the beginning while preserving the relative order of non-zero digits."
    input_format:
      type: string
      description: "A sequence of space-separated single digits."
      length: 12
      element_type: digit (0-9)
    output_format:
      type: string
      description: "A sequence of space-separated single digits, rearranged according to the rule."
      length: 12
      element_type: digit (0-9)
    transformation:
      action: partition
      elements: digits
      partition_key: "is zero"
      order_preservation:
        - group: non-zero digits
          preserve: relative order from input
        - group: zero digits
          order: does not matter (all are '0')
      concatenation_order:
        - group: zero digits
        - group: non-zero digits
      output_structure: "Concatenated groups formatted as space-separated digits."
    examples_summary:
      count: 7
      consistency: "All examples follow the same rearrangement pattern."
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of individual digits.
    2.  Create two new lists: one for zero digits (`zeros_list`) and one for non-zero digits (`non_zeros_list`).
    3.  Iterate through the input list of digits:
        *   If a digit is '0', append it to the `zeros_list`.
        *   If a digit is not '0', append it to the `non_zeros_list`.
    4.  Concatenate the `zeros_list` and the `non_zeros_list` in that order to form the final list of digits.
    5.  Join the digits in the final list with spaces to create the output string.