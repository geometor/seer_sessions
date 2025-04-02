"""
Shifts a single contiguous horizontal segment of a non-white color 3 positions to the right within a 1x25 grid, filling the remaining space with white (0).
"""

import numpy as np

def find_segment(grid):
    """Finds the start index, end index, and color of the first non-white segment."""
    segment_color = None
    start_index = -1
    end_index = -1
    width = grid.shape[1]

    for col in range(width):
        pixel = grid[0, col]
        if pixel != 0: # Found a non-white pixel
            if segment_color is None: # Start of the segment
                segment_color = pixel
                start_index = col
            elif pixel != segment_color: # Should not happen based on examples, but handle defensively
                break # End of segment if color changes (unexpected)
            end_index = col # Keep updating end index while in the segment
        elif segment_color is not None: # Found a white pixel after the segment started
            break # End of the segment

    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, length, segment_color
    else:
        return -1, 0, 0 # No segment found

def transform(input_grid):
    """
    Shifts a single contiguous horizontal segment of a non-white color 
    3 positions to the right within a 1x25 grid.

    Args:
        input_grid (np.array): A 1x25 numpy array representing the input grid.

    Returns:
        np.array: A 1x25 numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # Ensure it's 2D (1 row)
    if input_grid.ndim == 1:
        input_grid = input_grid.reshape(1, -1)
        
    rows, cols = input_grid.shape
    
    # Initialize output grid with the background color (white/0)
    output_grid = np.zeros_like(input_grid)

    # Find the non-white segment in the input grid
    start_index, length, segment_color = find_segment(input_grid)

    # If a segment was found
    if start_index != -1:
        # Calculate the new starting position (shift 3 to the right)
        new_start_index = start_index + 3

        # Determine the segment's end position in the output
        new_end_index = new_start_index + length

        # Ensure the new segment position is within the grid bounds
        # Although not strictly needed by examples, good practice
        if new_start_index < cols:
            # Place the segment in the output grid
            # Handle potential clipping at the right edge
            end_slice = min(new_end_index, cols)
            output_grid[0, new_start_index:end_slice] = segment_color

    return output_grid