import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies the two distinct non-white colors present in the input grid
    and swaps their positions. Background (white) pixels remain unchanged.

    Args:
      input_grid: A numpy array representing the input grid.

    Returns:
      A numpy array representing the output grid with the two non-white
      colors swapped.
    """

    # Find the unique non-zero color values in the input grid
    unique_colors = np.unique(input_grid)
    non_white_colors = unique_colors[unique_colors != 0]

    # Ensure there are exactly two non-white colors to swap
    if len(non_white_colors) != 2:
        # This case shouldn't happen based on the examples, but it's good practice
        # to handle it. We could raise an error or return the input unchanged.
        # Returning input unchanged seems safer for ARC tasks.
        print(f"Warning: Expected 2 non-white colors, found {len(non_white_colors)}. Returning original grid.")
        return input_grid.copy()

    color1 = non_white_colors[0]
    color2 = non_white_colors[1]

    # Create a copy of the input grid to modify
    output_grid = input_grid.copy()

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the color of the current cell
            current_color = input_grid[r, c]

            # Apply the swap logic
            if current_color == color1:
                output_grid[r, c] = color2
            elif current_color == color2:
                output_grid[r, c] = color1
            # White (0) pixels remain unchanged as the output grid is a copy

    return output_grid