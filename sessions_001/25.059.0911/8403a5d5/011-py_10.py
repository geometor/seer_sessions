def describe_grid(grid):
    """Provides a concise description of a grid."""
    rows, cols = grid.shape
    description = {
        'shape': (rows, cols),
        'min': int(np.min(grid)),
        'max': int(np.max(grid)),
        'unique_values': np.unique(grid).tolist(),
        'green_pixel': find_pixel_by_color(grid, 3)
    }

    return description