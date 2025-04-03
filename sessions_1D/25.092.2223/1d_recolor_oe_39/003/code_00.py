"""
Color transformation of azure objects based on sequence and separation.

This transformation operates on a 1D array (row vector) of pixels.
It identifies contiguous segments (objects) of azure (color 8) pixels against a white (color 0) background.
The background pixels (color 0) remain unchanged.
The transformation rule for azure objects depends on their order of appearance (left-to-right) and the length of the white gap preceding them:
1. The first azure object is always colored blue (1).
2. The second azure object is always colored gray (5).
3. For the third and subsequent azure objects:
    - If the gap of white pixels immediately preceding the object has a length of 3 or more, the object is colored blue (1).
    - Otherwise (gap length 0, 1, or 2), the object is colored gray (5).
The length of the array and the positions/shapes of the segments are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described color transformation to the input grid.

    Args:
        input_grid (list or np.array): A list, list of lists (with one inner list), 
                                       or numpy array representing the input pixels.

    Returns:
        list: A 1D list representing the transformed pixels.
    """
    # Ensure input is a flattened 1D numpy array
    grid = np.array(input_grid, dtype=int).flatten()
    
    # Initialize output_grid as a copy of the input grid.
    # This preserves background (0) pixels automatically.
    output_grid = grid.copy()

    # Initialize state variables
    object_index = 0       # Counter for azure objects found
    prev_object_end = -1   # Index immediately after the end of the previous azure object
    n = len(grid)          # Length of the grid
    i = 0                  # Current position in the grid

    # Iterate through the grid
    while i < n:
        # Check if the current pixel is azure (8)
        if grid[i] == 8:
            # Found the start of a potential azure object
            current_object_start = i
            
            # Check if it's *actually* the start of a new object 
            # (i.e., not a continuation of the previous one we might have iterated over)
            # This check simplifies because we jump 'i' forward after processing an object.
            # If grid[i] is 8, it must be the start of a new segment to process.
            
            object_index += 1
            
            # Determine the target color based on the object index and preceding gap
            target_color = -1 # Default/error value
            if object_index == 1:
                target_color = 1  # First object is blue
            elif object_index == 2:
                target_color = 5  # Second object is gray
            else: # Third object or later
                # Calculate the gap length before this object
                # Gap starts right after the previous object ends (prev_object_end)
                # Gap ends right before this object starts (current_object_start)
                gap_length = current_object_start - prev_object_end
                
                if gap_length >= 3:
                    target_color = 1  # Blue if gap is 3 or more
                else:
                    target_color = 5  # Gray if gap is less than 3

            # Find the end of the current contiguous azure object
            # Move 'j' to find where the sequence of 8s ends
            j = current_object_start
            while j < n and grid[j] == 8:
                j += 1
            current_object_end = j # j is now the index *after* the last 8

            # Color the entire object in the output grid with the target color
            output_grid[current_object_start:current_object_end] = target_color
            
            # Update the end position of the 'previous' object for the next iteration
            prev_object_end = current_object_end
            
            # Move the main loop index 'i' past the object we just processed
            i = current_object_end 
        
        else:
            # If the current pixel is not azure (it's white), just move to the next pixel
            i += 1

    # Return the modified grid as a standard Python list
    return output_grid.tolist()