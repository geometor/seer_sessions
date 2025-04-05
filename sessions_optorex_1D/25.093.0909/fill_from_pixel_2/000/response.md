*   **Perception of the elements:**
    *   The input and output are lists of single-digit integers.
    *   The core transformation involves conditionally replacing sequences of zeros ('0') at the beginning and/or end of the list.
    *   The replacement value is determined by the non-zero number adjacent to the sequence of zeros.
    *   The replacement only occurs under specific conditions related to the values of the first two distinct non-zero numbers (for the beginning) and the last two distinct non-zero numbers (for the end).

*   **YAML Facts:**
    
```yaml
    objects:
      - input_list:
          type: list
          contains: integers (0-9)
      - output_list:
          type: list
          contains: integers (0-9)
          derivation: modified version of input_list
      - element:
          type: integer
          value_range: 0-9
      - zero_sequence:
          type: sublist
          contains_only: 0
          location: start or end of input_list
      - non_zero_element:
          type: integer
          value_range: 1-9
          properties: [value, index]
      - first_non_zero:
          type: non_zero_element
          relation: earliest non_zero element in the list
      - second_non_zero:
          type: non_zero_element
          relation: second earliest non_zero element in the list (if exists)
      - last_non_zero:
          type: non_zero_element
          relation: latest non_zero element in the list
      - second_last_non_zero:
          type: non_zero_element
          relation: second latest non_zero element in the list (if exists)

    actions:
      - find_non_zeros:
          input: input_list
          output: list of (value, index) pairs for non_zero_elements
      - compare_values:
          input: two non_zero_elements
          output: boolean (equal or not equal)
      - fill_zeros:
          target: section of output_list (start or end)
          condition: comparison result of relevant non-zero elements
          value: value of the adjacent non_zero_element (first_non_zero or last_non_zero)

    relationships:
      - adjacency: A zero_sequence is adjacent to a non_zero_element at the start or end.
      - conditional_fill_start: The zero_sequence at the start is filled if the first_non_zero value differs from the second_non_zero value (or if only one non_zero element exists).
      - conditional_fill_end: The zero_sequence at the end is filled if the last_non_zero value differs from the second_last_non_zero value (or if only one non_zero element exists).
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input list to serve as the initial output list.
    2.  Identify all non-zero elements and their indices in the input list.
    3.  If there are no non-zero elements, return the output list unchanged.
    4.  Determine the first non-zero element (value `v1`, index `i1`) and the last non-zero element (value `vL`, index `iL`).
    5.  **Left Fill Check:**
        a.  Find the second non-zero element (value `v2`, index `i2`) if it exists.
        b.  If only one non-zero element exists OR if `v1` is not equal to `v2`, then replace all elements in the output list from index 0 up to (but not including) index `i1` with the value `v1`.
    6.  **Right Fill Check:**
        a.  Find the second-to-last non-zero element (value `vL-1`, index `iL-1`) if it exists.
        b.  If only one non-zero element exists OR if `vL` is not equal to `vL-1`, then replace all elements in the output list from index `iL + 1` to the end of the list with the value `vL`.
    7.  Return the modified output list.