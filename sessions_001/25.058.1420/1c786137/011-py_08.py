def get_grid_attributes(grid):
    """
    Analyzes a grid and returns relevant attributes.

    Args:
        grid: A 2D list representing the grid.

    Returns:
        A dictionary containing grid attributes.
    """
    import numpy as np

    grid_array = np.array(grid)
    height, width = grid_array.shape
    unique_colors = np.unique(grid_array)
    color_counts = {color: np.sum(grid_array == color) for color in unique_colors}

    return {
        "height": height,
        "width": width,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }