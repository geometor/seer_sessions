import numpy as np

def find_object_indices(grid):
    """Finds the start and end indices of a contiguous non-background block."""
    non_background_indices = np.where(grid != 0)[0]
    if len(non_background_indices) == 0:
        return None, None  # No object found
    start_index = non_background_indices[0]
    end_index = non_background_indices[-1]
    # Verify contiguity (optional but good practice)
    if not np.all(grid[start_index:end_index+1] != 0):
         # This check might be too strict if the "object" could internally contain background pixels.
         # Based on examples, the object is a solid block.
         # Consider refining if future examples show objects with holes.
         print("Warning: Non-contiguous non-background pixels detected.") # Or raise an error
         # For now, assume contiguity based on examples and return the found range.
         pass

    # Check if the found block matches the length of the indices
    expected_length = end_index - start_index + 1
    if len(non_background_indices) != expected_length:
         # This indicates gaps within what we identified as the block's bounds
         # or multiple separate blocks. The examples only show one solid block.
         print(f"Warning: Found indices {non_background_indices} do not form a single contiguous block between {start_index} and {end_index}.")
         # Based on task description, assume only one contiguous block exists.
         # The current logic correctly finds the overall span.
         pass


    return start_index, end_index

def transform(input_grid_list):
    """
    Moves a single contiguous block of non-background pixels (color 0)
    3 positions to the right within a 1D grid. The background remains
    white (color 0). Assumes the input is a 1D list or array.
    """
    # Convert input list to a numpy array for easier manipulation
    input_grid = np.array(input_grid_list)

    # Ensure it's 1D
    if input_grid.ndim > 1:
        # If it's a 1xN or Nx1 grid, flatten it. Otherwise, raise error or handle differently.
        if input_grid.shape[0] == 1 or input_grid.shape[1] == 1:
             input_grid = input_grid.flatten()
        else:
             raise ValueError("Input grid must be 1-dimensional or trivially flattenable (1xN or Nx1)")

    # Get grid size
    grid_size = len(input_grid)

    # Define background color
    background_color = 0

    # Find the start and end indices of the non-background object
    start_index, end_index = find_object_indices(input_grid)

    # If no object is found, return the original grid (or an empty one based on spec)
    if start_index is None:
        return input_grid_list # Return in original format

    # Create the output grid, initialized with the background color
    output_grid = np.full(grid_size, background_color, dtype=input_grid.dtype)

    # Define the shift amount
    shift_distance = 3

    # Calculate the new start and end indices
    new_start_index = start_index + shift_distance
    new_end_index = end_index + shift_distance

    # Check if the new position is within the grid boundaries
    if new_start_index < grid_size and new_end_index < grid_size :
        # Extract the object from the input grid
        object_pixels = input_grid[start_index:end_index + 1]

        # Place the object in the output grid at the new location
        output_grid[new_start_index:new_end_index + 1] = object_pixels
    else:
        # Handle cases where the shift would move the object partially or fully out of bounds.
        # Based on the examples, this doesn't seem to happen, but it's good to consider.
        # Option 1: Truncate the object if it hits the boundary.
        # Option 2: Wrap around (not suggested by examples).
        # Option 3: Return an error or a specific state.
        # Let's implement truncation for robustness, although not strictly needed for provided examples.

        # Calculate how much of the object fits
        object_pixels = input_grid[start_index:end_index + 1]
        placeable_length = grid_size - new_start_index
        if placeable_length > 0:
             output_grid[new_start_index:new_start_index + placeable_length] = object_pixels[:placeable_length]
        # If new_start_index is already >= grid_size, nothing gets placed.

    # Convert back to a list (as per ARC standard format often used)
    return output_grid.tolist()