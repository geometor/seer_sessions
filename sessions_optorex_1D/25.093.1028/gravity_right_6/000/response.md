*   **Perception of Elements:**
    *   The input consists of a sequence of integers, represented as a space-separated string. These integers can be zero or non-zero.
    *   The output is also a sequence of integers of the same length as the input, represented in the same format.
    *   The core elements are the individual integers within the sequence. A key property distinguishing them is whether they are zero or non-zero.

*   **YAML Fact Document:**
    
```yaml
    task_description: "Rearrange a sequence of integers by moving all zeros to the beginning."
    input_data:
      type: "string"
      format: "space-separated integers"
      elements:
        - type: "integer"
        properties:
          - value: "zero or non-zero"
          - original_position: "index in the sequence"
    output_data:
      type: "string"
      format: "space-separated integers"
      length: "same as input sequence"
    transformation:
      action: "partition and reorder"
      partition_criteria: "element value is zero or non-zero"
      reordering_rule: "place all zero elements first, then all non-zero elements"
      constraints:
        - "maintain relative order of non-zero elements"
        - "output length must match input length"
    relationships:
      - input_element -> output_element: "Each element from the input appears exactly once in the output."
      - non_zero_input_elements -> non_zero_output_elements: "The subsequence of non-zero elements in the output is identical to the subsequence of non-zero elements in the input."
      - zero_input_elements -> zero_output_elements: "The count of zero elements in the input equals the count of zero elements in the output."
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of integers.
    2.  Count the total number of elements in the input list.
    3.  Create two empty lists: one for zero elements (`zeros`) and one for non-zero elements (`non_zeros`).
    4.  Iterate through the input list of integers:
        *   If an element is zero, add it to the `zeros` list.
        *   If an element is non-zero, add it to the `non_zeros` list.
    5.  Concatenate the `zeros` list and the `non_zeros` list to form the output list.
    6.  Format the output list back into a space-separated string.