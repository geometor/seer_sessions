import numpy as np

"""
Transforms the input grid based on the width of the bounding box of the azure (8) object.
The input grid contains a single connected object made of azure pixels (8) on a white background (0).
The transformation identifies this object, calculates its bounding box width.
If the bounding box width is 6, it returns a specific predefined 5x5 pattern (Pattern A).
If the bounding box width is 5, it returns a different predefined 5x5 pattern (Pattern B).
"""

# Define the two possible output patterns as numpy arrays for potential future manipulation,
# though they are returned as lists of lists.
PATTERN_A = np.array([
    [8, 8, 0, 8, 8],
    [8, 8, 0, 8, 8],
    [0, 0, 0, 0, 0],
    [8, 8, 0, 8, 8],
    [8, 8, 0, 8, 8]
], dtype=int)

PATTERN_B = np.array([
    [0, 8, 0, 0, 8],
    [8, 8, 0, 8, 8],
    [0, 0, 0, 0, 0],
    [0, 8, 0, 0, 8],
    [8, 8, 0, 8, 8]
], dtype=int)

AZURE_COLOR = 8
DEFAULT_OUTPUT_SIZE = (5, 5)

def find_pixels(grid, color):
    """Finds the coordinates of all pixels matching the given color."""
    # np.argwhere returns coordinates as [row, col] pairs
    coords = np.argwhere(grid == color)
    return coords

def calculate_bounding_box(coords):
    """
    Calculates the bounding box (min_row, max_row, min_col, max_col) 
    from a numpy array of coordinates. Returns None if coords is empty.
    """
    if coords.size == 0:
        return None 

    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Applies the transformation rule based on the azure object's bounding box width.
    
    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed 5x5 output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # 1. & 2. Identify all azure cells and their coordinates.
    azure_coords = find_pixels(input_np, AZURE_COLOR)

    # Handle case where no azure pixels are found (robustness)
    if azure_coords.size == 0:
        print("Warning: No azure pixels found in input. Returning default empty grid.")
        return np.zeros(DEFAULT_OUTPUT_SIZE, dtype=int).tolist()

    # 3. Determine the bounding box.
    bbox = calculate_bounding_box(azure_coords)
    # bbox is (min_row, max_row, min_col, max_col)
    
    # Should not happen if azure_coords is not empty, but check for safety
    if bbox is None:
        print("Warning: Could not calculate bounding box. Returning default empty grid.")
        return np.zeros(DEFAULT_OUTPUT_SIZE, dtype=int).tolist()

    # 4. Calculate the width of the bounding box.
    # Width = max_col - min_col + 1
    width = bbox[3] - bbox[2] + 1

    # 5. Check the width and select the corresponding output pattern.
    if width == 6:
        # Select Pattern A
        output_grid = PATTERN_A.copy() 
    elif width == 5:
        # Select Pattern B
        output_grid = PATTERN_B.copy()
    else:
        # Fallback for unexpected widths based on observed examples
        print(f"Warning: Unexpected bounding box width {width}. Returning default empty grid.")
        output_grid = np.zeros(DEFAULT_OUTPUT_SIZE, dtype=int)

    # 6. Return the selected 5x5 grid as a list of lists.
    return output_grid.tolist()