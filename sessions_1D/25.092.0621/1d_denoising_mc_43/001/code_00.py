import collections
import copy
import numpy as np # Using numpy for easier array handling, though list slicing works too

"""
Identifies a contiguous segment of non-white (non-zero) pixels within a single-row input grid.
Determines the most frequent non-white color (dominant color) within that segment.
Replaces all pixels within the identified segment in the output grid with the dominant color.
Leaves any leading or trailing white (zero) pixels unchanged.
"""

def transform(input_grid):
    """
    Transforms a single-row grid by homogenizing the color of its central non-white segment.

    Args:
        input_grid (list of lists): A list containing a single list of integers representing pixels.

    Returns:
        list of lists: The transformed grid with the non-white segment homogenized.
    """
    # Ensure input is treated as a 1D array/list
    if not isinstance(input_grid, np.ndarray):
      input_grid = np.array(input_grid)

    if input_grid.shape[0] != 1:
        # This function is designed for single-row inputs based on examples
        # Handle error or adapt if multi-row inputs are possible
        raise ValueError("Input grid must have exactly one row.")

    row = input_grid[0]
    output_grid = np.copy(input_grid) # Use numpy copy
    output_row = output_grid[0]
    n = len(row)

    # --- 1. Identify the contiguous segment of non-white pixels ---
    start_index = -1
    end_index = -1
    non_white_indices = np.where(row != 0)[0] # Find indices of all non-zero elements

    if non_white_indices.size > 0:
        start_index = non_white_indices[0]
        end_index = non_white_indices[-1]
    else:
        # If no non-white pixels, return the original grid
        return output_grid.tolist() # Return as list of lists

    # --- 2. Determine the dominant color within this non-white segment ---
    # Extract the segment (only non-white pixels matter for counting dominance)
    segment = row[start_index : end_index + 1]
    
    # Count occurrences of each non-white color within the segment
    # Filter out 0s before counting if needed, but Counter naturally handles it
    color_counts = collections.Counter(c for c in segment if c != 0)

    # Check if the segment contained only white pixels (shouldn't happen based on segment definition)
    if not color_counts:
        return output_grid.tolist() # Return original if segment had no non-white pixels

    # Find the color with the highest count
    dominant_color = color_counts.most_common(1)[0][0]

    # --- 3. Create the output row ---
    # (Already created output_grid/output_row as a copy)

    # --- 4 & 5. Iterate through the segment in the output and set to dominant color ---
    # Modify the output row in place
    for i in range(start_index, end_index + 1):
         output_row[i] = dominant_color
         
    # --- 6. Leave padding unchanged ---
    # This happens automatically as we only modified the segment indices.

    # --- 7. Return the modified grid ---
    return output_grid.tolist() # Convert back to list of lists format
