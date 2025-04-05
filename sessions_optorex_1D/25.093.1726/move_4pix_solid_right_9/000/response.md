*   **Perception:** The task involves transforming a sequence of 12 numbers. The input sequences contain groups of identical non-zero numbers (or single non-zero numbers) surrounded by zeros. The transformation appears to move these non-zero numbers to the right within the sequence. The amount of shift seems constant across all examples. Zeros fill the space vacated by the shifted numbers and the original positions not occupied by shifted numbers.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: list_of_integers
        length: 12
        properties: contains_non_zero_elements
      - name: output_sequence
        type: list_of_integers
        length: 12
        properties: derived_from_input
      - name: non_zero_element
        type: integer
        properties: value, position_index
      - name: zero_element
        type: integer
        value: 0
    actions:
      - name: shift_right
        actor: system
        object: non_zero_element
        amount: 4_positions
        constraints: stays_within_sequence_bounds
      - name: fill_with_zeros
        actor: system
        object: output_sequence
        locations: indices_not_occupied_by_shifted_elements
    relationships:
      - type: positional_mapping
        source: non_zero_element in input_sequence at index `i`
        target: same non_zero_element in output_sequence at index `i + 4`
    constants:
      - sequence_length: 12
      - shift_amount: 4
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of 12 zeros.
    2.  Iterate through the input sequence from index 0 to 11.
    3.  For each element at index `i` in the input sequence:
        a.  If the element is non-zero:
            i.  Calculate the target index `j` as `i + 4`.
            ii. If the target index `j` is within the bounds of the sequence (less than 12), place the non-zero element at index `j` in the output sequence.
    4.  Return the resulting output sequence.