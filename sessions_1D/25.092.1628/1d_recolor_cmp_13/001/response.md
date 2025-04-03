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