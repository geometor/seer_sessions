*   **Perception of Task Elements:**
    *   The input and output are both 1-dimensional sequences (or lists) of integers.
    *   Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros.
    *   The output sequence retains the same non-zero digits and the same number of zeros as the input.
    *   The primary transformation is the positional shift of the non-zero block within the sequence.
    *   The length of the sequence remains constant between input and output.
    *   The non-zero block consistently shifts 3 positions to the right.

*   **YAML Documentation of Facts:**
    
```yaml
    task_description: "Shift a contiguous block of identical non-zero digits within a sequence."
    elements:
      - element: sequence
        description: "A 1-dimensional list of integers."
        properties:
          - length: "Constant between input and output (12 in examples)."
          - contains_zeros: true
          - contains_non_zero_block: true
      - element: non_zero_block
        description: "A contiguous sub-sequence of identical digits greater than zero."
        properties:
          - digit_value: "The repeated non-zero integer (e.g., 7, 9, 5, 8)."
          - length: "Variable (e.g., 2, 3, 4, 5)."
          - start_index: "The starting position of the block in the input sequence."
          - end_index: "The ending position of the block in the input sequence."
    action:
      - name: shift_right
        target: non_zero_block
        properties:
          - amount: 3
          - direction: right
        effect: "Moves the non_zero_block 3 positions towards the end of the sequence."
    relationships:
      - type: positional
        description: "The non_zero_block occupies a new set of indices in the output sequence, shifted relative to its input position."
      - type: replacement
        description: "The original positions of the non_zero_block in the input are filled with zeros in the output."
    constraints:
      - "The sequence length remains unchanged."
      - "Only one non-zero block exists per sequence."
      - "The shift amount is fixed at 3 positions to the right."
      - "No wrap-around behavior is observed in the examples."

    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero digits in the input sequence. Determine its value, length, and starting index.
    2.  Create a new output sequence of the same length as the input, initialized entirely with zeros.
    3.  Calculate the new starting index for the block by adding 3 to its original starting index.
    4.  Copy the identified non-zero block into the output sequence, starting at the calculated new index.
    5.  Return the modified output sequence.