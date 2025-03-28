import numpy as np

def find_bounding_box(grid):
    """
    Finds the minimum bounding box containing all non-background (non-zero) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if no non-background pixels exist.
    """
    non_background_pixels = np.where(grid != 0)
    rows = non_background_pixels[0]
    cols = non_background_pixels[1]

    if len(rows) == 0:
        return None  # No non-background pixels found

    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the subgrid defined by the minimal bounding box containing all non-white pixels.

    1. Identify all pixels in the input grid that are not white (value 0).
    2. Determine the minimum and maximum row and column indices occupied by these non-white pixels.
       This defines the bounding box.
    3. Create the output grid by copying the portion of the input grid within this bounding box.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Find the bounding box of non-white pixels
    bbox = find_bounding_box(input_array)

    # If no non-white pixels are found, return an empty grid or a default
    # Based on examples, we expect non-white pixels. If not, maybe return a 1x1 white grid?
    # For now, let's assume the bounding box is always found for valid inputs.
    if bbox is None:
        # Handle the case where the input grid is all white (or empty)
        # Returning a 1x1 white grid seems like a reasonable default, though not explicitly shown.
        return [[0]] 
        # Or perhaps return an empty list: return []

    min_row, max_row, min_col, max_col = bbox

    # Extract the subgrid corresponding to the bounding box
    output_array = input_array[min_row : max_row + 1, min_col : max_col + 1]

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid