
## train_1

**input:**
```
0 8 8 8 0 0 8 8 8 8 8 0 0 8 8 8 8 8 0 8 8 0 0 8 8 0 8 8 8 8 8
```


**output:**
```
0 8 8 8 0 0 3 3 3 3 3 0 0 3 3 3 3 3 0 8 8 0 0 8 8 0 3 3 3 3 3
```


## train_2

**input:**
```
0 0 0 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8 0 0 8 8 8 0 0 8 8 8 8 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 3 3 0 3 3 3 3 3 3 3 0 0 8 8 8 0 0 8 8 8 8 0 0
```


## train_3

**input:**
```
0 0 8 8 8 0 0 0 8 8 8 0 8 8 8 8 0 8 8 8 8 0 0 8 8 8 0 8 8 8 8
```


**output:**
```
0 0 8 8 8 0 0 0 8 8 8 0 3 3 3 3 0 3 3 3 3 0 0 8 8 8 0 3 3 3 3
```

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
```python
import numpy as np
from typing import List, Tuple, Dict

"""
Identify all contiguous horizontal sequences of azure (8) pixels in the input row.
Determine the maximum length among these sequences.
Change the color of only those azure sequences that have this maximum length to green (3).
Leave all other pixels (white (0) and shorter azure sequences) unchanged.
"""

def find_color_sequences(row: List[int], target_color: int) -> List[Dict[str, int]]:
    """
    Finds all contiguous sequences of a target color in a 1D list (row).

    Args:
        row: The input list of pixel values.
        target_color: The color value to search for sequences of.

    Returns:
        A list of dictionaries, where each dictionary represents a sequence
        and contains 'start', 'end', and 'length' keys.
    """
    sequences = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == target_color:
            if start_index == -1:
                start_index = i  # Start of a new sequence
        elif start_index != -1:
            # End of the current sequence
            sequences.append({
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            start_index = -1  # Reset for the next sequence

    # Check if the row ends with a sequence
    if start_index != -1:
        sequences.append({
            'start': start_index,
            'end': len(row) - 1,
            'length': len(row) - start_index
        })

    return sequences

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by changing the color of the longest sequences
    of azure (8) pixels to green (3).

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed output row.
    """
    # Input is expected to be a single row grid
    if not input_grid or not input_grid[0]:
        return input_grid # Return empty or invalid input as is

    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy for the output

    # 1. Find all contiguous sequences of azure (8) pixels
    azure_sequences = find_color_sequences(input_row, 8)

    # If no azure sequences are found, return the original grid
    if not azure_sequences:
        return input_grid

    # 2. Determine the maximum length among the azure sequences
    max_length = 0
    for seq in azure_sequences:
        if seq['length'] > max_length:
            max_length = seq['length']

    # 3. Iterate through the sequences and change color if length matches max_length
    for seq in azure_sequences:
        if seq['length'] == max_length:
            # 4. Change pixels in the output row for maximal sequences
            for i in range(seq['start'], seq['end'] + 1):
                output_row[i] = 3 # Change to green

    # Wrap the output row back into the grid format
    output_grid = [output_row]
    return output_grid

```
