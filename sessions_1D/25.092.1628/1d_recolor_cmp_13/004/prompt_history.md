
## train_1

**input:**
```
0 0 1 0 1 1 1 1 0 1 1 1 1 0 0 1 1 1 1 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 1 0 7 7 7 7 0 7 7 7 7 0 0 7 7 7 7 0 0 0 1 1 1 0 0 0
```


## train_2

**input:**
```
0 0 0 1 1 1 1 1 0 0 1 1 1 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 0 0 1 1 1 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 0 1 1 1 1 1 1 1 0 1 1 1 0 0 1 1 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 1 1 0 7 7 7 7 7 7 7 0 1 1 1 0 0 1 1 1 1 1 0 0 0 0 0
```

*   **Perception:** The task involves processing a single-row grid. The input grid contains sequences of white (0) and blue (1) pixels. The output grid shows that some sequences of blue pixels have been changed to orange (7), while others remain blue. White pixels are unchanged. Specifically, contiguous horizontal sequences of exactly four blue pixels are transformed into sequences of four orange pixels. Blue sequences of other lengths (like the single blue pixel and the sequence of three blue pixels) are left untouched.

*   **Facts:**
    
```yaml
    task_type: color_change_conditional
    grid_dimensionality: 1D # Effectively 1D as it's a single row
    objects:
      - type: sequence
        color: blue (1)
        attributes:
          - length
    actions:
      - type: color_change
        source_color: blue (1)
        target_color: orange (7)
        condition: Applies only to blue sequences with a length of exactly 4.
    background: white (0) pixels remain unchanged.
    unchanged_elements:
      - blue (1) sequences with lengths other than 4.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input grid to identify contiguous horizontal sequences of blue (1) pixels.
    2.  For each identified blue sequence, determine its length.
    3.  If the length of a blue sequence is exactly 4, change the color of all pixels within that specific sequence to orange (7) in the output grid.
    4.  If the length of a blue sequence is not 4, keep the pixels as blue (1) in the output grid.
    5.  Copy all other pixels (white pixels) directly from the input to the output grid without modification.
```python
import copy

"""
Iterate through the input grid (which is a single row) to identify contiguous 
horizontal sequences of blue (1) pixels. If a sequence of blue pixels has a length 
of exactly 4, change the color of all pixels within that sequence to orange (7) 
in the output grid. All other pixels (white pixels and blue sequences of lengths 
other than 4) remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule: change sequences of 4 blue pixels to orange.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists of integers. 
                                      Expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Ensure the input grid has at least one row
    if not input_grid or not input_grid[0]:
        return []

    # Work with the first row as it's effectively a 1D problem
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy for the output
    
    cols = len(input_row)
    i = 0 # Current index in the row

    # Iterate through the row to find sequences
    while i < cols:
        # Check if the current pixel is blue (1)
        if input_row[i] == 1:
            # Find the end of the contiguous blue sequence starting at i
            start_index = i
            j = i
            while j < cols and input_row[j] == 1:
                j += 1
            
            sequence_length = j - start_index
            
            # Check if the sequence length is exactly 4
            if sequence_length == 4:
                # Change the pixels in the output row to orange (7) for this sequence
                for k in range(start_index, j):
                    output_row[k] = 7
            
            # Move the main index past this processed sequence
            i = j 
        else:
            # If the current pixel is not blue, just move to the next pixel
            i += 1
            
    # Return the transformed row within a list to match the grid format
    return [output_row]

```
```python
import copy
import numpy as np # Using numpy for potential convenience, though list operations suffice

"""
Identify all contiguous horizontal sequences of blue (1) pixels in the input row. 
Determine the maximum length (L_max) among these sequences. 
Change all blue sequences whose length equals L_max to orange (7). 
Leave all other pixels (white pixels and blue sequences with length != L_max) unchanged.
"""

def find_blue_sequences(input_row):
    """
    Finds all contiguous sequences of blue (1) pixels in a row.

    Args:
        input_row (list[int]): A list representing a single row of the grid.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a 
                    sequence with keys 'start' (index) and 'length'. 
                    Returns an empty list if no blue sequences are found.
    """
    sequences = []
    cols = len(input_row)
    i = 0
    while i < cols:
        if input_row[i] == 1: # Start of a potential blue sequence
            start_index = i
            j = i
            # Find the end of the sequence
            while j < cols and input_row[j] == 1:
                j += 1
            sequence_length = j - start_index
            sequences.append({'start': start_index, 'length': sequence_length})
            i = j # Move index past the found sequence
        else:
            i += 1 # Move to the next pixel
    return sequences

def transform(input_grid):
    """
    Transforms the input grid based on the rule: change the longest blue sequences to orange.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists of integers.
                                      Expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy for the output

    # Step 1 & 2: Find all blue sequences and their lengths
    blue_sequences = find_blue_sequences(input_row)

    # Step 3: Determine the maximum length
    max_length = 0
    if blue_sequences:
        max_length = max(seq['length'] for seq in blue_sequences)

    # Step 4 & 5 & 6: Apply transformation based on max length
    if max_length > 0: # Only proceed if there are blue sequences
        for seq in blue_sequences:
            # If the sequence length is the maximum length
            if seq['length'] == max_length:
                start = seq['start']
                length = seq['length']
                # Change the corresponding pixels in the output row to orange (7)
                for k in range(start, start + length):
                    # Check bounds just in case, though logic should prevent overrun
                    if k < len(output_row): 
                        output_row[k] = 7

    # Step 7 & 8: Return the modified row in grid format
    return [output_row]

```
