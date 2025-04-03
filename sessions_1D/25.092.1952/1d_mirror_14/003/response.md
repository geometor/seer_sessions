```python
"""
1. Create the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
2. Identify the unique row (`target_row_index`) in the input grid that contains both the single maroon pixel (9) and the single contiguous segment of non-white, non-maroon pixels.
3. Locate the column index (`pivot_col_index`) of the maroon pixel (9) within the `target_row_index`. Place this maroon pixel at (`target_row_index`, `pivot_col_index`) in the output grid.
4. Identify the contiguous segment of pixels within the `target_row_index` that are not white (0) and not maroon (9). Note their color (`object_color`) and their column indices (`object_col_indices`) in the input grid.
5. For each column index `c` in the `object_col_indices`:
   a. Calculate the reflected column index `reflected_col_index = (2 * pivot_col_index) - c`.
   b. Place the `object_color` at the position (`target_row_index`, `reflected_col_index`) in the output grid.
6. Return the completed output grid.
"""

import numpy as np

def find_relevant_row_and_pivot(grid):
    """
    Finds the row containing both the pivot (9) and the object (non-0, non-9),
    and returns the row index and the pivot's column index.
    """
    pivot_pos = None
    object_rows = set()
    object_pixels = {} # Store potential object pixel locations (r, c) -> color

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            pixel = grid[r, c]
            if pixel == 9:
                if pivot_pos is not None:
                    raise ValueError("Multiple pivot pixels (9) found.")
                pivot_pos = (r, c)
            elif pixel != 0:
                object_rows.add(r)
                object_pixels[(r,c)] = pixel

    if pivot_pos is None:
        raise ValueError("Pivot pixel (9) not found.")

    pivot_row, pivot_col = pivot_pos

    # Check if the pivot row contains any object pixels
    object_found_in_pivot_row = any(r == pivot_row for r, c in object_pixels)

    if not object_found_in_pivot_row:
         raise ValueError(f"No object pixels found in the pivot row ({pivot_row}).")
         
    # Verify that all object pixels are ONLY in the pivot row
    if not all(r == pivot_row for r in object_rows):
         raise ValueError("Object pixels found outside the pivot row.")


    return pivot_row, pivot_col

def find_object_in_row(grid, row_index, pivot_col_index):
    """
    Finds the color and column indices of the contiguous object
    in the specified row, excluding the pivot position.
    """
    object_color = None
    object_col_indices = []
    row_data = grid[row_index]
    
    current_segment_indices = []
    
    for c in range(len(row_data)):
        pixel = row_data[c]
        # Skip background (0) and pivot (9)
        if pixel != 0 and pixel != 9:
            if object_color is None:
                 object_color = pixel # First object pixel found
            
            if pixel == object_color:
                current_segment_indices.append(c)
            else: 
                 # Found a different color - this implies multiple objects or error
                 # Based on examples, we assume one contiguous object color
                 # If we already found an object, stop looking
                 if object_col_indices:
                     break 
                 else: # This is the start of a new segment of a different color
                      # Reset and start tracking the new color
                      object_color = pixel
                      current_segment_indices = [c]

        elif current_segment_indices: # End of the current segment
            # Check if the segment just ended was the target object color
             if grid[row_index, current_segment_indices[0]] == object_color:
                object_col_indices = current_segment_indices
                # Found the contiguous segment, we can potentially break if we assume only one
                # For robustness, let's continue scanning but only store the first valid segment
                break # Assuming only one object segment per relevant row based on examples
             else:
                current_segment_indices = [] # Reset segment tracking


    # Handle case where the object segment runs to the end of the row
    if current_segment_indices and not object_col_indices:
         if grid[row_index, current_segment_indices[0]] == object_color:
              object_col_indices = current_segment_indices


    if object_color is None or not object_col_indices:
        raise ValueError(f"Contiguous object not found in row {row_index} excluding pivot.")
        
    # Final check for contiguity (redundant if loop logic is perfect, but safe)
    if len(object_col_indices) > 1:
        for i in range(len(object_col_indices) - 1):
            if object_col_indices[i+1] != object_col_indices[i] + 1:
                 raise ValueError(f"Detected object in row {row_index} is not contiguous.")

    return object_color, object_col_indices


def transform(input_grid_list):
    """
    Transforms the input grid by reflecting a colored horizontal object segment
    across a stationary pivot pixel (9) within the same row.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Find the relevant row and the pivot's column index
    try:
        target_row_index, pivot_col_index = find_relevant_row_and_pivot(input_grid)
    except ValueError as e:
        print(f"Error identifying pivot/object row: {e}")
        # Depending on requirements, might return input, empty, or raise error
        # For now, let's return an empty grid of same size if structure is wrong.
        return np.zeros_like(input_grid).tolist()


    # Place the pivot pixel (9) in the output grid
    output_grid[target_row_index, pivot_col_index] = 9

    # Find the object's color and column indices in the relevant row
    try:
        object_color, object_col_indices = find_object_in_row(input_grid, target_row_index, pivot_col_index)
    except ValueError as e:
        print(f"Error identifying object in row {target_row_index}: {e}")
        # If object isn't found but pivot is, place pivot and return
        return output_grid.tolist()


    # Calculate reflected positions and place the object in the output grid
    for c in object_col_indices:
        # Calculate reflection relative to the pivot column
        reflected_col_index = 2 * pivot_col_index - c

        # Check bounds before placing the pixel
        if 0 <= reflected_col_index < width:
            output_grid[target_row_index, reflected_col_index] = object_color
        else:
            # This case indicates reflection goes out of bounds.
            # Based on examples, this shouldn't happen, but good to handle.
            print(f"Warning: Reflected column index {reflected_col_index} for original column {c} in row {target_row_index} is out of bounds.")

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```