*   **Perception of Elements:**
    *   The input and output are sequences (or lists) of 12 single-digit integers.
    *   Each input sequence contains a contiguous block of identical non-zero digits, surrounded by zeros.
    *   The output sequence contains the same block of non-zero digits as the input, but its position within the sequence has changed. The remaining elements are zeros.
*   **YAML Facts:**
    
```yaml
    task_elements:
      - type: sequence
        length: 12
        element_type: integer
        range: 0-9
    input_structure:
      - contains: background
        value: 0
      - contains: object
        description: A contiguous block of identical non-zero digits.
        properties:
          - value: non-zero integer (constant within the block)
          - length: variable
          - position: variable
    output_structure:
      - contains: background
        value: 0
      - contains: object
        description: The same object from the input sequence.
        properties:
          - value: same as input object
          - length: same as input object
          - position: shifted relative to input
    transformation:
      - action: identify_object
        target: the contiguous block of non-zero digits
      - action: shift_object
        direction: left
        magnitude: 4 positions
      - action: maintain_background
        value: 0
      - action: handle_boundaries
        description: Positions vacated by the shift are filled with 0. Elements shifted beyond the start boundary are implicitly discarded (though not observed in examples). Elements to the left of the original object remain 0 until potentially overwritten by the shifted object.

    ```

*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero numbers within the input sequence. Note its starting position, length, and the digit value.
    2.  Create a new output sequence of the same length (12), initially filled with zeros.
    3.  Calculate the new starting position for the block by subtracting 4 from its original starting position in the input.
    4.  Place the identified block of non-zero digits into the output sequence, starting at the calculated new position. Ensure the block maintains its original length and digit value.