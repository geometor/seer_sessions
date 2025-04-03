```python
"""
Iterate through the input array from left to right.
Identify contiguous segments of azure (8) pixels. Keep track of the start index and length of each segment.
For each identified azure segment:
    a. Determine the length of the segment.
    b. Select the replacement color based on the length:
        *   If the length is 1, use orange (7).
        *   If the length is 2, use green (3).
        *   If the length is 3, use red (2).
    c. Replace the pixels corresponding to the identified segment in the input array (or a copy) with the selected replacement color.
Pixels that were originally white (0) remain white (0).
The resulting array is the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing contiguous segments of azure pixels (8)
    with segments of the same length but different colors based on the segment length.
    Length 1 -> orange (7), Length 2 -> green (3), Length 3 -> red (2).
    Other pixels remain unchanged.

    Args:
        input_grid (list): A 1D list representing the input grid.

    Returns:
        list: A 1D list representing the transformed grid.
    """
    # Convert input list to a numpy array for easier slicing and assignment
    # Use int dtype as ARC colors are integers 0-9
    grid = np.array(input_grid, dtype=int) 
    # Create a copy to store the output, initialized with the input grid values
    output_grid = grid.copy()

    # Define the mapping from segment length to the replacement color
    length_to_color_map = {
        1: 7,  # orange
        2: 3,  # green
        3: 2,  # red
    }
    # Define the target color to find segments of
    target_color = 8 # azure

    i = 0
    n = len(grid)
    # Iterate through the grid using an index 'i'
    while i < n:
        # Check if the current pixel matches the target color (azure)
        if grid[i] == target_color:
            # Found the start of a potential target color segment
            start_index = i
            segment_length = 0
            # Count the length of the contiguous target color segment
            # Continue incrementing 'i' as long as we are within the grid bounds
            # and the pixel color matches the target color
            while i < n and grid[i] == target_color:
                segment_length += 1
                i += 1
            # The segment ends either because we hit a different color or the end of the grid
            
            # Check if the measured segment length has a defined replacement color in our map
            if segment_length in length_to_color_map:
                replacement_color = length_to_color_map[segment_length]
                # Replace the segment in the output grid with the calculated replacement color
                # Numpy slicing [start_index:i] covers the correct range
                output_grid[start_index:i] = replacement_color
            # If the segment length is not in the map (e.g., > 3), 
            # it remains unchanged in the output_grid (as it was copied initially).
            # 'i' is already advanced past the segment by the inner loop, so the outer loop continues correctly.
        else:
            # If the current pixel is not the target color, just move to the next pixel
            i += 1

    # Convert the final numpy array back to a list, as per typical ARC output format
    return output_grid.tolist()
```