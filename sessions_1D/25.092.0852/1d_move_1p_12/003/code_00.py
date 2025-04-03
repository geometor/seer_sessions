"""
Identifies a single contiguous horizontal segment of non-white pixels 
in the first row of the input 2D grid and shifts this segment one 
position to the right in the output grid. The rest of the grid remains white (0).
The dimensions, color, and length of the segment are preserved.
"""

import numpy as np

def find_segment_in_row(row: np.ndarray) -> tuple[int, int, int]:
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white segment in a 1D NumPy array (row).

    Args:
        row: A 1D NumPy array representing a row of pixel colors.

    Returns:
        A tuple containing:
        - start_index: The starting column index of the segment. -1 if no segment found.
        - end_index: The ending column index of the segment. -1 if no segment found.
        - color: The color of the segment pixels. 0 if no segment found.
    """
    start = -1
    end = -1
    color = 0
    in_segment = False
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if not in_segment:
                # Start of a new segment
                start = i
                color = pixel
                in_segment = True
            end = i  # Update end index as long as we are in the segment
        elif in_segment:
            # Just exited the segment
            break  # Assume only one segment per row based on examples
            
    return start, end, color

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the non-white segment in the first row 
    one position to the right.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape
    
    # Initialize the output grid with the same shape, filled with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Check if the grid has at least one row
    if height > 0:
        # Extract the first row
        first_row = input_grid[0, :]
        
        # Find the segment in the first row
        start_index, end_index, segment_color = find_segment_in_row(first_row)

        # Check if a segment was found
        if start_index != -1:
            # Calculate the new starting position (shifted right by 1)
            new_start_index = start_index + 1
            
            # Calculate the length of the segment
            segment_length = end_index - start_index + 1

            # Place the shifted segment into the first row of the output grid
            for i in range(segment_length):
                # Calculate the target column index in the output grid
                current_output_col = new_start_index + i
                
                # Check bounds to ensure we don't write outside the grid width
                if 0 <= current_output_col < width:
                    output_grid[0, current_output_col] = segment_color
                else:
                    # Stop if the segment goes off the edge (though not expected based on examples)
                    break
                    
    # Return the transformed grid
    return output_grid