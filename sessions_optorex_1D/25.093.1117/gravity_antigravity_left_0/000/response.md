*   **Perception:** The task involves rearranging a sequence of twelve digits (0, 1, or 2). The output sequence contains the exact same digits as the input sequence, but sorted according to a specific custom order. The length of the sequence remains unchanged.

*   **Facts:**
    
```yaml
    task_type: rearrangement
    input_elements:
      type: sequence
      data_type: integer
      possible_values: [0, 1, 2]
      length: 12
    output_elements:
      type: sequence
      data_type: integer
      possible_values: [0, 1, 2]
      length: 12
    relationship:
      - The output sequence is a permutation of the input sequence.
      - The count of each distinct digit (0, 1, 2) is preserved between input and output.
      - The output sequence is sorted based on a custom key: 2 comes first, followed by 0, then 1.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of twelve digits.
    2.  Count the occurrences of the digit '2' in the input sequence.
    3.  Count the occurrences of the digit '0' in the input sequence.
    4.  Count the occurrences of the digit '1' in the input sequence.
    5.  Construct the output sequence by concatenating:
        *   The digit '2' repeated according to its count.
        *   The digit '0' repeated according to its count.
        *   The digit '1' repeated according to its count.
    6.  Return the resulting sequence.