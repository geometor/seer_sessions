*   **Perception of Elements:**
    *   The input and output are both lists of integers.
    *   The input list contains only 0s and 1s.
    *   The output list contains 0s, 1s, and 3s.
    *   The lengths of the input and output lists are always the same.
    *   The transformation seems conditional. In many cases (train\_2 through train\_7), the output is identical to the input.
    *   In train\_1, a change occurs: specific 0s in the input are replaced by 3s in the output.
    *   The change in train\_1 seems related to the presence of the subsequence `1 1`. Specifically, 0s immediately adjacent to a `1 1` subsequence (`0 1 1 0`) are replaced by 3s.

*   **Facts:**
    
```yaml
    task_elements:
      - object: input_list
        properties:
          - type: list
          - element_type: integer
          - allowed_values: [0, 1]
          - length: variable (but consistent within a pair)
      - object: output_list
        properties:
          - type: list
          - element_type: integer
          - allowed_values: [0, 1, 3]
          - length: same as input_list
      - object: pattern
        properties:
          - value: [1, 1]
          - context: subsequence within input_list
      - object: target_pattern
        properties:
          - value: [0, 1, 1, 0]
          - context: subsequence within input_list
          - role: trigger for transformation
      - action: copy_elements
        description: Elements from the input list are generally copied to the output list unless a specific condition is met.
      - action: replace_elements
        description: Specific 0s in the input list are replaced by 3s in the output list.
        condition: The 0 is part of the `target_pattern` [0, 1, 1, 0].
        target: The leading and trailing 0s of the `target_pattern`.
        replacement_value: 3
      - relationship: identity
        description: If the `target_pattern` [0, 1, 1, 0] is not found in the input_list, the output_list is identical to the input_list.
      - relationship: transformation
        description: If the `target_pattern` [0, 1, 1, 0] is found, the corresponding 0s at the start and end of the pattern in the input are changed to 3s in the output, while the central [1, 1] remains unchanged. Other elements are copied.
    ```


*   **Natural Language Program:**
    1.  Initialize the output list as a copy of the input list.
    2.  Iterate through the input list, examining subsequences of length 4.
    3.  For each position `i` from 0 up to `length - 4`:
        a.  Check if the subsequence starting at index `i` matches the pattern `[0, 1, 1, 0]`.
        b.  If the pattern matches:
            i.  Change the element at index `i` in the output list to 3.
            ii. Change the element at index `i + 3` in the output list to 3.
    4.  Return the modified output list.