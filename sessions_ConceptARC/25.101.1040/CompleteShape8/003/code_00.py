import numpy as np

"""
Transformation rule:
1. Create an output grid of the same size as the input, initialized to white (0).
2. Identify all unique non-white (0) and non-gray (5) colors present in the input grid.
3. For each such unique color:
    a. Find the coordinates of all pixels in the input grid having this color.
    b. Calculate the minimum bounding box enclosing all these pixels.
    c. Determine the height and width of this bounding box.
    d. If the bounding box height is exactly 3 and the width is exactly 3:
        i. Fill the entire 3x3 bounding box area in the output grid with this color.
    e. Otherwise (if the bounding box is not 3x3):
        i. Copy only the pixels at the original coordinates (found in step 3a) to the output grid using this color.
4. Gray (5) pixels from the input are effectively removed because they are not processed and the output starts as white.
5. Return the final output grid.
"""

def get_bounding_box(coords: np.ndarray) -> tuple[int, int, int, int, int, int]:
    """
    Calculates the bounding box and its dimensions for a set of coordinates.

    Args:
        coords: A NumPy array of shape (N, 2) containing (row, col) coordinates.

    Returns:
        A tuple containing (min_row, min_col, max_row, max_col, height, width).
        Returns (-1, -1, -1, -1, 0, 0) if coords is empty.
    """
    if coords.shape[0] == 0:
        return -1, -1, -1, -1, 0, 0

    min_row = np.min(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_row = np.max(coords[:, 0])
    max_col = np.max(coords[:, 1])

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, max_row, max_col, height, width

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Removes gray pixels, identifies non-gray color groups, and either fills their
    3x3 bounding box or copies their original pixels based on the bounding box size.
    """
    # Convert input to NumPy array
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output grid with background color (white=0)
    output_array = np.zeros_like(input_array, dtype=int)

    # Find unique colors in the input, excluding background (0) and gray (5)
    unique_colors = np.unique(input_array)
    colors_to_process = [c for c in unique_colors if c != 0 and c != 5]

    # Process each relevant color
    for color in colors_to_process:
        # Find all coordinates for the current color
        coords = np.argwhere(input_array == color)

        # If the color exists in the grid
        if coords.shape[0] > 0:
            # Calculate bounding box and dimensions
            min_r, min_c, max_r, max_c, height, width = get_bounding_box(coords)

            # Check if the bounding box is exactly 3x3
            if height == 3 and width == 3:
                # Fill the 3x3 bounding box in the output grid
                # Ensure indices are within bounds (though calculation should be correct)
                fill_min_r = max(0, min_r)
                fill_min_c = max(0, min_c)
                fill_max_r = min(rows, max_r + 1)
                fill_max_c = min(cols, max_c + 1)
                output_array[fill_min_r:fill_max_r, fill_min_c:fill_max_c] = color
            else:
                # Otherwise, copy the original object pixels to the output grid
                # coords is already a list of [row, col] pairs
                for r, c in coords:
                    output_array[r, c] = color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid