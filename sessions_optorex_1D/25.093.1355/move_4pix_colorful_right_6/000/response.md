*   **Perception:** The task involves transforming a sequence of 12 integers. Observing the input and output pairs reveals a consistent pattern: the entire sequence of numbers in the input is shifted to the right by a fixed number of positions. The positions vacated at the beginning of the sequence are filled with zeros, and elements shifted beyond the end of the sequence are discarded, maintaining the original length of 12. Across all examples, the magnitude of the right shift is consistently 4 positions.

*   **Facts:**
    
```yaml
    task: sequence_transformation
    input:
      data_type: sequence
      element_type: integer
      length: 12
      properties:
        - contains zeros and non-zero integers
    output:
      data_type: sequence
      element_type: integer
      length: 12
      properties:
        - derived from input sequence
    transformation:
      action: right_shift
      parameters:
        shift_amount: 4
        fill_value: 0
      constraints:
        - preserve original sequence length (12)
        - prepend fill_value for vacated positions
        - truncate elements shifted beyond original length
    relationship:
      - output is the result of applying a fixed right shift of 4 positions to the input sequence, padding with zeros at the start and truncating at the end.
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of 12 integers.
    2.  Perform a right shift operation on the entire sequence by 4 positions.
    3.  Prepend 4 zeros to the beginning of the shifted sequence.
    4.  Keep only the first 12 elements of the resulting sequence, discarding any elements shifted beyond the 12th position.
    5.  The resulting sequence of 12 integers is the output.