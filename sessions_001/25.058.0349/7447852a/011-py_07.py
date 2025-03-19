def compare_grids(grid1, grid2):
    """
    Compares two grids and returns the differences.

    Args:
      grid1: The first grid (NumPy array).
      grid2: The second grid (NumPy array).

    Returns:
      A tuple containing:
        - A boolean indicating whether the grids are identical.
        - A list of tuples, where each tuple represents a differing cell
          and contains: (row_index, col_index, value_in_grid1, value_in_grid2)
    """
    if grid1.shape != grid2.shape:
        return False, "Different Shapes"

    diffs = []
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                diffs.append((i, j, grid1[i, j], grid2[i, j]))

    return len(diffs) == 0, diffs