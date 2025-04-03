import numpy as np

"""
Transforms a 1D input grid (list of integers) based on the following rules:
1. Identifies a single maroon (9) pixel which acts as a fixed pivot point.
2. Identifies a single contiguous block (object) of a non-white (0), non-maroon (9) color.
3. Calculates the gap (number of white pixels) between the object and the maroon pivot.
4. Moves the object to the opposite side of the maroon pivot in the output grid, maintaining the original gap size.
5. The output grid has the same dimensions as the input, with the maroon pivot in its original position and the object relocated. All other pixels are white (0).
"""

def find_pixel_index(grid_1d, color):
    """Finds the index of the first occurrence of a specific color in a list."""
    try:
        return grid_1d.index(color)
    except ValueError:
        return -1 # Color not found

def find_object_details(grid_1d, ignore_colors=(0, 9)):
    """
    Finds the details (color, start_idx, end_idx) of the first 
    contiguous object made of a color not in ignore_colors.
    Returns (None, -1, -1) if no such object is found.
    """
    start_idx = -1
    object_color = -1
    for idx, pixel in enumerate(grid_1d):
        # Start of a potential object
        if pixel not in ignore_colors and start_idx == -1:
            start_idx = idx
            object_color = pixel
        # Continuation of the object - do nothing
        elif pixel == object_color and start_idx != -1:
            continue
        # End of the object (pixel changed to something else)
        elif pixel != object_color and start_idx != -1:
            return object_color, start_idx, idx - 1
            
    # Handle case where object goes to the end of the grid
    if start_idx != -1:
        return object_color, start_idx, len(grid_1d) - 1
        
    # No object found
    return None, -1, -1

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list or numpy array representing the 1D input grid. 
                     Can also be a list containing a single list (like [[...]]).

    Returns:
        A list representing the transformed 1D output grid.
    """
    # --- Input Parsing and Validation ---
    # Handle cases where input might be list of list or numpy array
    if isinstance(input_grid, np.ndarray):
        # If it's a 2D numpy array with 1 row, flatten it
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
             grid_1d = input_grid[0].tolist()
        # If it's already 1D numpy array
        elif input_grid.ndim == 1:
             grid_1d = input_grid.tolist()
        else:
             # Handle unexpected numpy array shape if necessary
             raise ValueError("Input numpy array has unexpected dimensions.")
    elif isinstance(input_grid, list):
         # If it's a list containing a single list [[...]]
        if len(input_grid) == 1 and isinstance(input_grid[0], list):
            grid_1d = input_grid[0]
        # Assume it's already a flat list [...]
        elif all(isinstance(item, int) for item in input_grid):
             grid_1d = input_grid
        else:
             raise ValueError("Input list has unexpected format.")
    else:
        raise TypeError("Input grid must be a list or numpy array.")

    grid_length = len(grid_1d)

    # --- Find Key Elements ---
    # Find the pivot (maroon pixel)
    pivot_index = find_pixel_index(grid_1d, 9)
    if pivot_index == -1:
        # Handle error: Pivot not found (should not happen based on examples)
        # Return input or raise error depending on desired behavior
        print("Warning: Maroon pivot (9) not found in input.")
        return grid_1d 

    # Find the object
    object_color, start_idx, end_idx = find_object_details(grid_1d)
    if object_color is None:
        # Handle error: Object not found (should not happen based on examples)
        print("Warning: Movable object not found in input.")
        return grid_1d # Or perhaps return a grid with only the pivot?

    object_length = end_idx - start_idx + 1

    # --- Calculate Transformation Parameters ---
    # Determine object position relative to pivot and calculate gap size
    gap_size = 0
    object_on_left = False
    if end_idx < pivot_index:
        object_on_left = True
        gap_size = pivot_index - end_idx - 1
    elif start_idx > pivot_index:
        object_on_left = False
        gap_size = start_idx - pivot_index - 1
    else:
        # This case (object overlapping pivot) shouldn't occur based on examples
        print("Warning: Object overlaps or touches pivot.")
        return grid_1d # Or handle as error

    # --- Construct Output Grid ---
    # Initialize output grid with background color (white)
    output_grid = [0] * grid_length

    # Place the pivot in the output
    output_grid[pivot_index] = 9

    # Calculate new position for the object
    new_start_idx = -1
    if object_on_left:
        # Original object was left, move it to the right
        new_start_idx = pivot_index + gap_size + 1
    else:
        # Original object was right, move it to the left
        new_end_idx = pivot_index - gap_size - 1
        new_start_idx = new_end_idx - object_length + 1

    # Calculate the new end index based on the calculated start index
    new_end_idx = new_start_idx + object_length - 1

    # --- Validate and Place Object ---
    # Check if the calculated new position is valid within the grid boundaries
    if 0 <= new_start_idx <= new_end_idx < grid_length:
        # Place the object in the output grid
        for i in range(new_start_idx, new_end_idx + 1):
            output_grid[i] = object_color
    else:
        # Handle error: New position is out of bounds
        print(f"Error: Calculated new object position [{new_start_idx}, {new_end_idx}] is out of bounds for grid length {grid_length}.")
        # Fallback: return the grid with only the pivot placed
        output_grid = [0] * grid_length
        output_grid[pivot_index] = 9


    return output_grid