import numpy as np

"""
Identify pairs of pixels of the same non-background color within each row of the input grid. 
For each such pair found in a row, fill the horizontal segment between the pair's column indices (inclusive) with that color in the corresponding row of the output grid. 
Rows without exactly two pixels of the same non-background color remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by filling horizontal segments between pairs of same-colored pixels in each row.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid.
    # Modifications will be made directly to this copy.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each row of the grid.
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the column indices and colors of non-background pixels in the current row.
        non_background_indices = np.where(row != 0)[0]
        
        # If there are no non-background pixels, continue to the next row.
        if len(non_background_indices) == 0:
            continue

        # Group the column indices by their color.
        color_indices_map = {}
        for col_idx in non_background_indices:
            color = row[col_idx]
            if color not in color_indices_map:
                color_indices_map[color] = []
            color_indices_map[color].append(col_idx)

        # Process each color group found in the row.
        for color, indices in color_indices_map.items():
            # Check if there are exactly two pixels of this specific color in the row.
            if len(indices) == 2:
                # Determine the minimum (leftmost) and maximum (rightmost) column index for the pair.
                min_col = min(indices)
                max_col = max(indices)
                
                # Fill the horizontal segment between min_col and max_col (inclusive) 
                # in the corresponding row of the output grid with the pair's color.
                output_grid[r, min_col : max_col + 1] = color

    # Return the modified grid.
    return output_grid
