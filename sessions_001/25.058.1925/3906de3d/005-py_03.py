def describe_grid(grid):
    """
    Provides a basic description of objects in a grid.
    """
    unique, counts = np.unique(grid, return_counts=True)
    object_descriptions = []
    for color, count in zip(unique, counts):
        if color != 0:  # Ignore background
          coords = np.argwhere(grid == color)
          min_row, min_col = np.min(coords, axis = 0)
          max_row, max_col = np.max(coords, axis = 0)
          width = max_col - min_col + 1
          height = max_row - min_row + 1
          object_descriptions.append(
              f"Color {color}: Count={count}, Top-Left=({min_row},{min_col}), Bottom-Right=({max_row},{max_col}), Width={width}, Height={height}"
            )
    return "\n".join(object_descriptions)