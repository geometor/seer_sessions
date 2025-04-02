import copy
import numpy as np

def find_non_white_pixels(row):
    """Finds indices and the single color of non-white pixels in a row."""
    non_white_indices = []
    pixel_color = 0  # Default to white/background
    found_first_color = False
    for index, pixel in enumerate(row):
        if pixel != 0:
            non_white_indices.append(index)
            if not found_first_color:
                pixel_color = pixel
                found_first_color = True
            elif pixel != pixel_color:
                # Handle error or unexpected condition: multiple non-white colors
                # Based on examples, this shouldn't happen.
                # For robustness, could raise an error or return a specific signal.
                pass 
    return non_white_indices, pixel_color

def transform(input_grid):
    """
    Identifies pairs of non-white pixels in a 1D input grid (represented as a 1xN grid)
    and fills the segment between each pair (inclusive) with their color.

    Assumptions based on training examples:
    - Input is a list containing one row (list or sequence).
    - The row contains an even number of non-white pixels.
    - All non-white pixels share the same color.
    - Pixels between pairs are initially white (0).
    """
    
    # Ensure input is structured as expected (list of one list/sequence)
    if not isinstance(input_grid, (list, np.ndarray)) or len(input_grid) != 1:
        # Return input unchanged if structure is unexpected
        return input_grid

    # Create a deep copy to avoid modifying the original input
    # Using np.array ensures mutability for element assignment
    try:
        output_grid = np.array(input_grid, dtype=int)
    except Exception:
        # Fallback if numpy conversion fails (e.g., ragged list, though unlikely for ARC)
        output_grid = copy.deepcopy(input_grid)


    # Extract the row (now definitely mutable if numpy was successful)
    # If numpy failed, we need to ensure the inner list is mutable
    if isinstance(output_grid, np.ndarray):
         # With numpy, slicing often returns a view, but assignment modifies the original array
         # Direct access output_grid[0] is fine for modification
         pass
    elif isinstance(output_grid[0], list):
         # It's already a list, should be mutable
         pass
    else:
         # If it's a tuple or other immutable sequence, convert it to list
         try:
            output_grid[0] = list(output_grid[0])
         except TypeError:
             # If conversion fails, we cannot modify; return the copy
             return output_grid

    input_row = output_grid[0] # Work directly on the row within the output_grid

    # 1. Find the indices and the color of all non-white pixels
    non_white_indices, pixel_color = find_non_white_pixels(input_row)

    # 2. Check if non-white pixels were found and count is even
    if not non_white_indices or len(non_white_indices) % 2 != 0:
        # Return the unmodified copy if conditions aren't met
        # Convert back to list of lists if we used numpy
        if isinstance(output_grid, np.ndarray):
             return output_grid.tolist()
        else:
             return output_grid

    # 3. Group indices into pairs and fill segments
    # Iterate through the found indices, taking two at a time
    for i in range(0, len(non_white_indices), 2):
        # Check if there's a matching pair index
        if i + 1 < len(non_white_indices):
            start_index = non_white_indices[i]
            end_index = non_white_indices[i+1]

            # Fill the segment in the output row, from start_index to end_index inclusive
            # Use slicing for numpy arrays for efficiency, otherwise loop
            if isinstance(output_grid, np.ndarray):
                if 0 <= start_index <= end_index < output_grid.shape[1]:
                    output_grid[0, start_index : end_index + 1] = pixel_color
            else:
                 # Standard list modification
                for j in range(start_index, end_index + 1):
                    # Ensure index j is within the bounds of the row
                    if 0 <= j < len(input_row):
                        input_row[j] = pixel_color # Modifies the row within output_grid

    # 4. Return the modified grid
    # Convert back to list of lists format if we used numpy
    if isinstance(output_grid, np.ndarray):
        return output_grid.tolist()
    else:
        return output_grid