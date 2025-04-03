Okay, let's analyze the provided examples.

## Perception of Task Elements

1.  **Input/Output Format:** The input and output are both single rows (1D grids) of pixels.
2.  **Colors Involved:** The colors present are white (0), azure (8), and green (3). White pixels appear as background/separators. Azure pixels are the primary objects being manipulated. Green pixels appear only in the output as a result of transformation.
3.  **Transformation:** The core transformation involves changing *some* sequences of azure pixels (8) to green pixels (3). White pixels (0) always remain unchanged. Not all azure sequences are changed; some remain azure in the output.
4.  **Identifying the Rule:** The key is determining *which* azure sequences are changed. Comparing the lengths of the azure sequences in the input and observing which ones change reveals a pattern:
    *   In `train_1`, the longest azure sequences have length 5. Only sequences of length 5 are changed to green. Shorter sequences (lengths 2 and 3) remain azure.
    *   In `train_2`, the longest azure sequences have length 7. Only sequences of length 7 are changed to green. Shorter sequences (lengths 3 and 4) remain azure.
    *   In `train_3`, the longest azure sequences have length 4. Only sequences of length 4 are changed to green. Shorter sequences (length 3) remain azure.
5.  **Conclusion:** The transformation rule seems to be: identify all contiguous horizontal sequences of azure pixels, find the maximum length among these sequences, and then change only those sequences that have this maximum length to green. All other pixels (white pixels and azure sequences shorter than the maximum length) remain unchanged.

## YAML Fact Document


```yaml
task_context:
  grid_dimensionality: 1D (single row)
  colors_used:
    - white (0)
    - azure (8)
    - green (3)
  input_composition: Primarily sequences of azure pixels separated by white pixels.
  output_composition: Similar structure to input, but some azure sequences are replaced by green sequences.

objects:
  - type: pixel
    properties:
      - color: (white: 0, azure: 8, green: 3)
      - position: index in the row
  - type: sequence
    properties:
      - color: azure (8)
      - pixels: list of contiguous pixels of the same color
      - length: number of pixels in the sequence
      - start_index: position of the first pixel
      - end_index: position of the last pixel
      - is_maximal_length: boolean indicating if its length equals the maximum length of all azure sequences in the row

actions_on_objects:
  - action: identify_sequences
    description: Find all contiguous horizontal sequences of azure (8) pixels in the input row.
    input: input row
    output: list of azure sequences with their properties (length, position)
  - action: find_max_length
    description: Determine the maximum length among all identified azure sequences.
    input: list of azure sequences
    output: maximum length value
  - action: filter_maximal_sequences
    description: Identify which sequences have a length equal to the maximum length.
    input: list of azure sequences, maximum length value
    output: list of maximal-length azure sequences
  - action: change_color
    description: Change the color of pixels within the identified maximal-length sequences from azure (8) to green (3).
    input: input row, list of maximal-length sequences
    output: modified output row

relationships:
  - type: contiguity
    description: Pixels of the same color adjacent horizontally form a sequence.
  - type: comparison
    description: The length of each azure sequence is compared to the maximum length found across all azure sequences in that specific input row.

invariants:
  - White (0) pixels remain unchanged in position and color.
  - Azure (8) sequences whose length is less than the maximum length for that input row remain unchanged.
  - The length and position of the modified sequences remain the same, only the color changes.
  - The overall length of the row remains unchanged.

transformation_goal: To highlight the longest contiguous sequence(s) of azure pixels by changing their color to green.
```


## Natural Language Program

1.  Scan the input row to identify all contiguous horizontal sequences of azure (8) pixels. Record the starting position and length of each sequence.
2.  Determine the maximum length found among all the identified azure sequences in the input row.
3.  Iterate through the identified azure sequences again.
4.  For each azure sequence, compare its length to the maximum length determined in step 2.
5.  If an azure sequence's length is equal to the maximum length, change the color of all pixels within that sequence in the output row to green (3).
6.  If an azure sequence's length is less than the maximum length, keep the color of all pixels within that sequence as azure (8) in the output row.
7.  Ensure all white (0) pixels from the input row are copied to the output row in their original positions.
8.  The final modified row is the result.