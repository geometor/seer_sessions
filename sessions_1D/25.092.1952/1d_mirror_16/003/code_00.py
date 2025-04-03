"""
Transforms a 1D numpy array based on a pivot and object mirroring rule with a conditional gap.

The transformation identifies a single maroon pixel (9) which acts as a pivot. 
It then finds the contiguous block of a single non-white, non-maroon color located immediately to the left 
of a potential gap of white pixels (0), which itself is immediately to the left of the pivot.
The size of this 'left gap' (number of white pixels between the object/start and the pivot) is measured.

An output array of the same size is created, initially filled with white pixels (0).
The pivot (9) is placed in the output array at its original index.

The transformation then calculates a 'right gap' size. If the identified colored block started at 
index 0 in the input array, the 'right gap' size equals the 'left gap' size. Otherwise (if the block 
started at index > 0, or if no block was found adjacent to the left gap), the 'right gap' size is 
the 'left gap' size plus one.

Finally, the identified colored block is placed in the output array, starting immediately after the 
calculated 'right gap' (i.e., starting at index: pivot_index + 1 + right_gap_size). 
All other positions in the output array remain white (0).
"""

import numpy as np

def find_pivot(grid_np):
  """Finds the index of the pivot color (9). Returns -1 if not found."""
  pivot_indices = np.where(grid_np == 9)[0]
  if len(pivot_indices) == 1:
    return pivot_indices[0]
  else:
    # Handle cases where the pivot is not found or multiple pivots exist.
    # Based on examples, a single pivot should exist.
    return -1 

def find_object_and_left_gap(grid_np, pivot_index):
    """
    Finds the object (contiguous non-white, non-pivot block) and the gap 
    to the left of the pivot.
    Returns the object pixels (list), object start index, and the left gap size.
    Returns (None, -1, left_gap_size) if no valid object is found.
    """
    object_pixels = []
    object_start_index = -1
    left_gap_size = 0
    
    # 1. Calculate left_gap_size by scanning left from pivot
    current_index = pivot_index - 1
    while current_index >= 0 and grid_np[current_index] == 0:
        left_gap_size += 1
        current_index -= 1
        
    # 2. Find the object
    # current_index is now at the potential last pixel of the object, or < 0
    object_found = False
    if current_index >= 0:
         object_color = grid_np[current_index]
         # Check if the color is valid (not white 0, not pivot 9)
         if object_color != 0 and object_color != 9:
             # Scan left to find the start of the object and collect pixels
             obj_idx = current_index
             while obj_idx >= 0 and grid_np[obj_idx] == object_color:
                 object_pixels.insert(0, grid_np[obj_idx]) # Prepend to keep order
                 object_start_index = obj_idx
                 obj_idx -= 1
             object_found = True

    if not object_found:
        return None, -1, left_gap_size
    else:
         return object_pixels, object_start_index, left_gap_size

def transform(input_grid):
    """
    Applies the pivot-mirror transformation with conditional gap logic.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid)
    input_len = len(input_np)
    
    # Initialize output_grid with white pixels (0)
    output_grid = np.zeros(input_len, dtype=int)

    # Find the pivot's position
    pivot_index = find_pivot(input_np)
    
    if pivot_index == -1:
      # If no pivot, return the empty grid (or handle as error)
      print("Warning: Pivot (9) not found in input.")
      return output_grid.tolist() # Return as list per ARC standard

    # Place the pivot in the output grid
    if 0 <= pivot_index < input_len:
        output_grid[pivot_index] = 9
    else:
        # Should not happen if find_pivot works correctly
        print("Error: Invalid pivot index.")
        return np.zeros(input_len, dtype=int).tolist()

    # Find the object and gap to the left of the pivot
    movable_object_pixels, object_start_index, left_gap_size = find_object_and_left_gap(input_np, pivot_index)

    # Determine the right gap size based on the conditional rule
    # If no object was found adjacent to the gap, object_start_index remains -1.
    starts_with_object = (object_start_index == 0)
    right_gap_size = left_gap_size if starts_with_object else left_gap_size + 1
        
    # Place the object in the output grid if it was found
    if movable_object_pixels is not None:
        object_len = len(movable_object_pixels)
        # Calculate the starting position for the object in the output grid
        output_object_start_index = pivot_index + 1 + right_gap_size
        
        # Place the object pixels, checking boundaries
        for i in range(object_len):
            output_index = output_object_start_index + i
            # Check if the index is within the output grid bounds
            if 0 <= output_index < input_len:
                output_grid[output_index] = movable_object_pixels[i]
            else:
                # Object goes out of bounds, stop placing.
                # Based on examples, this doesn't seem to happen.
                # print(f"Warning: Object placement out of bounds at index {output_index}.")
                break 

    # The output_grid is already filled with 0s for background and gaps.
    # Convert back to list for ARC standard output format.
    return output_grid.tolist()