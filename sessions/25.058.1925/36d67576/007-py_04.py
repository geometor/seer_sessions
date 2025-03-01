def code_execution(input_grid, output_grid):
    """
    Calculates and returns the differences between two grids.

    Args:
      input_grid: A numpy array representing the input grid.
      output_grid: A numpy array representing the output grid.

    Returns:
      A dictionary containing:
        - 'different_positions': A list of (row, col) tuples where the grids differ.
        - 'input_unique_colors': A list of the unique colors present in the input grid.
        - 'output_unique_colors': A list of the unique colors present in the output grid.
        - 'input_grid_size' : tuple of (row, col) indicating the size of the grid.
        - 'output_grid_size' : tuple of (row, col) indicating the size of the grid.
    """
    different_positions = []
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] != output_grid[r,c]:
          different_positions.append((r,c))

    input_unique_colors = np.unique(input_grid).tolist()
    output_unique_colors = np.unique(output_grid).tolist()

    return {
        'different_positions': different_positions,
        'input_unique_colors': input_unique_colors,
        'output_unique_colors': output_unique_colors,
        'input_grid_size':input_grid.shape,
        'output_grid_size': output_grid.shape,
    }