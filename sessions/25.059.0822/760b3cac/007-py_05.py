import numpy as np

def code_execution(input_grid, output_grid, transformed_grid):
    """
    Executes code and documents differences.
    Focus on location and color of differences.

    Args:
        input_grid:  The original input grid.
        output_grid: The expected output grid.
        transformed_grid: The output from the current transform function.

    Returns:
        A string describing the discrepancies.
    """

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    transformed_grid = np.array(transformed_grid)

    report = []
    if not np.array_equal(output_grid, transformed_grid):
        diff_indices = np.where(output_grid != transformed_grid)
        for r, c in zip(*diff_indices):
            report.append(
                f"Row: {r}, Col: {c}, Expected: {output_grid[r, c]}, Got: {transformed_grid[r, c]}"
            )
        if len(report) == 0:
            report.append("Output and Transformed are the same size, but pixel values differ in areas beyond simple row/col comparison")

    else:
      report.append("output_grid and transformed_grid are identical.")

    return "\n".join(report)