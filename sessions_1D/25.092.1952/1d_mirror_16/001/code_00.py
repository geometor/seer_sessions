import numpy as np # Although not strictly necessary for 1D lists, it's common in ARC tasks

"""
The transformation identifies a single maroon pixel (9) which acts as a pivot. 
It then finds the contiguous block of a single non-white, non-maroon color located to the left of the pivot. 
This block might be separated from the pivot by a gap of one or more white pixels (0).
The transformation moves this colored block to the right side of the pivot, preserving the size of the gap (number of white pixels) between the pivot and the block. 
The pivot itself remains in its original position relative to the grid boundaries. 
All other positions in the output grid are filled with white (0).
"""

def find_pivot(grid):
  """Finds the index of the pivot color (9)."""
  try:
    return grid.index(9)
  except ValueError:
    # Handle cases where the pivot is not found, though based on examples it should be.
    return -1 

def find_object_and_gap_left_of_pivot(grid, pivot_index):
    """
    Finds the object (contiguous non-white, non-pivot block) and the gap 
    to the left of the pivot.
    Returns the object (list of pixel values), its start index, and the gap size.
    """
    movable_object = []
    object_color = -1 
    object_start_index = -1
    gap_size = 0
    
    # 1. Calculate gap size
    current_index = pivot_index - 1
    while current_index >= 0 and grid[current_index] == 0:
        gap_size += 1
        current_index -= 1
        
    # 2. Find the object
    # current_index is now at the last pixel of the object, or -1 if no object found before start
    object_end_index = current_index
    if object_end_index >= 0:
         object_color = grid[object_end_index]
         # Check if the color is valid (not white 0, not pivot 9)
         if object_color != 0 and object_color != 9:
             # Scan left to find the start of the object
             while current_index >= 0 and grid[current_index] == object_color:
                 movable_object.insert(0, grid[current_index]) # Prepend to keep order
                 object_start_index = current_index
                 current_index -= 1
         else:
             # Found white or pivot where object expected, reset
             movable_object = []
             object_start_index = -1

    # If no valid object color was found right after the gap
    if not movable_object:
        object_start_index = -1 # Ensure index is invalid if no object

    return movable_object, object_start_index, gap_size

def transform(input_grid):
    """
    Moves the colored block left of the maroon pivot (9) to the right, 
    preserving the gap size.
    """
    input_len = len(input_grid)
    # Initialize output_grid with white pixels (0)
    output_grid = [0] * input_len

    # Find the pivot's position
    pivot_index = find_pivot(input_grid)
    
    if pivot_index == -1:
      # If no pivot, return the empty grid (or handle as error)
      # Based on examples, pivot always exists.
      print("Warning: Pivot (9) not found in input.")
      return output_grid # Or raise an error

    # Place the pivot in the output grid
    if 0 <= pivot_index < input_len:
        output_grid[pivot_index] = 9
    else:
        # Should not happen if find_pivot works correctly
        print("Error: Invalid pivot index.")
        return [0] * input_len


    # Find the object and gap to the left of the pivot
    movable_object, object_start_index, gap_size = find_object_and_gap_left_of_pivot(input_grid, pivot_index)

    # Check if an object was found
    if movable_object:
        object_len = len(movable_object)
        # Calculate the starting position for the object in the output grid
        output_object_start_index = pivot_index + 1 + gap_size
        
        # Place the object in the output grid, checking boundaries
        for i in range(object_len):
            output_index = output_object_start_index + i
            if 0 <= output_index < input_len:
                output_grid[output_index] = movable_object[i]
            else:
                # Object goes out of bounds, truncate or handle error
                # Based on examples, this doesn't seem to happen.
                print(f"Warning: Object placement out of bounds at index {output_index}.")
                break # Stop placing if out of bounds

    # The output_grid is already filled with 0s, so the gap and remaining space are handled.
    
    return output_grid