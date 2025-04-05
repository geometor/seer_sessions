## Perception of Task Elements

The task involves transforming a sequence of 12 single-digit integers.
*   **Input/Output:** Both input and output are fixed-length sequences (length 12) of single digits.
*   **Structure:** The sequences consist primarily of zeros (0) and a single contiguous block of identical non-zero digits (e.g., `1 1`, `9 9 9 9`, `3 3`).
*   **Transformation:** The core operation appears to be a spatial shift of the non-zero block within the sequence. The block moves towards the beginning of the sequence (left shift).
*   **Consistency:** The non-zero digit value and the length of the non-zero block remain unchanged between input and output. The shift amount seems constant across all examples.

## Documented Facts


```yaml
objects:
  - type: sequence
    properties:
      - element_type: integer (single digit, 0-9)
      - length: 12
  - type: block
    properties:
      - contiguity: true # elements are adjacent
      - element_value: non-zero (constant within the block)
      - location: defined by start and end index within the sequence
      - exists_within: sequence

relationships:
  - block_is_part_of: sequence
  - input_sequence -> output_sequence: transformation applied

actions:
  - identify: locate the non-zero block within the input sequence (find start index, end index, and value)
  - shift: move the identified block to a new location in the output sequence
    properties:
      - direction: left (towards index 0)
      - magnitude: 3 positions
  - preserve: maintain the value and length of the non-zero block
  - fill: ensure positions outside the shifted block in the output sequence are zero

constants:
  - sequence_length: 12
  - shift_amount: 3
  - shift_direction: left
```


## Natural Language Program

1.  Receive the input sequence of 12 digits.
2.  Identify the contiguous block of identical non-zero digits within the input sequence. Determine its starting index, its ending index, and the value of the digits in the block.
3.  Create a new output sequence of 12 digits, initially filled entirely with zeros.
4.  Calculate the new starting index for the block by subtracting 3 from its original starting index in the input sequence.
5.  Copy the identified block of non-zero digits from the input sequence into the output sequence, placing it starting at the newly calculated index.