import numpy as np

def code_execution(grids):
    """
    Executes the existing transform function on each grid in the input list.
    Returns a report comparing generated output to actual
    """
    results = {}
    report = ""
    
    def get_separator_indices(grid, separator_color=5):
        """Finds the column indices of separator pixels."""
        return np.where(grid == separator_color)[1]

    def transform(input_grid):
        """Transforms the input grid according to the observed rules."""
        output_grid = np.copy(input_grid)
        rows, cols = input_grid.shape

        # 1. Identify Separators
        separator_indices = get_separator_indices(input_grid)

        # Handle cases with no or one separator
        if len(separator_indices) == 0:
            return output_grid  # No separators, no change
        
        first_separator = separator_indices[0]
        last_separator = separator_indices[-1]

        # 2. Left Region
        output_grid[:, :first_separator] = 8

        # 3. Middle Region (only if there's more than one separator)
        if len(separator_indices) > 1:
            output_grid[:, first_separator + 1:last_separator] = 6

        # 4. Right Region
        output_grid[:, last_separator + 1:] = 9
        
        # 5. Preserve grey separators
        output_grid[input_grid == 5] = 5 # ensure separators are kept

        return output_grid

    for grid_idx, (input_grid, output_grid) in enumerate(grids):
        report += f"Example {grid_idx + 1}:\n"
        transformed_grid = transform(input_grid)
        comparison = np.array_equal(transformed_grid, output_grid)
        report += f"  Correct Output: {comparison}\n"
        if not comparison:
            incorrect_pixels = np.where(transformed_grid != output_grid)
            report += f"  Incorrect Pixels: {len(incorrect_pixels[0])}\n"
            # example incorrect pixel
            if len(incorrect_pixels[0]) > 0:
                first_incorrect_row = incorrect_pixels[0][0]
                first_incorrect_col = incorrect_pixels[1][0]
                report += f"  Sample Incorrect - Row: {first_incorrect_row}, Col: {first_incorrect_col}, Expected: {output_grid[first_incorrect_row, first_incorrect_col]}, Got: {transformed_grid[first_incorrect_row, first_incorrect_col]}\n"       
        results[f"example_{grid_idx + 1}"] = {
            "correct": comparison,
            "incorrect_pixels": np.where(transformed_grid != output_grid) if not comparison else None
        }
        report += "\n"

    return report

# get the example grids from the prompt
grids = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 5, 0, 0, 0, 0],
               [0, 0, 0, 0, 5, 0, 0, 0, 0],
               [0, 0, 0, 0, 5, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[8, 8, 8, 8, 5, 9, 9, 9, 9],
               [8, 8, 8, 8, 5, 9, 9, 9, 9],
               [8, 8, 8, 8, 5, 9, 9, 9, 9],
               [8, 8, 8, 8, 5, 9, 9, 9, 9],
               [8, 8, 8, 8, 8, 8, 8, 8, 8]])),
    (np.array([[5, 0, 0, 0, 0, 0, 0, 0, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 5, 0, 0, 0, 5, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [5, 0, 0, 0, 0, 0, 0, 0, 5]]),
     np.array([[5, 6, 6, 6, 6, 6, 6, 6, 5],
               [8, 8, 8, 8, 8, 8, 8, 8, 8],
               [8, 8, 5, 6, 6, 6, 5, 9, 9],
               [8, 8, 8, 8, 8, 8, 8, 8, 8],
               [5, 6, 6, 6, 6, 6, 6, 6, 5]])),
    (np.array([[0, 0, 5, 0, 0, 0, 0, 0, 0],
               [0, 0, 5, 5, 5, 5, 0, 0, 0],
               [0, 0, 0, 0, 0, 5, 5, 5, 0],
               [0, 0, 5, 0, 0, 0, 0, 0, 0],
               [0, 0, 5, 0, 0, 0, 0, 0, 0]]),
     np.array([[8, 8, 5, 9, 9, 9, 9, 9, 9],
               [8, 8, 5, 5, 5, 5, 9, 9, 9],
               [8, 8, 8, 8, 8, 5, 5, 5, 9],
               [8, 8, 5, 9, 9, 9, 9, 9, 9],
               [8, 8, 5, 9, 9, 9, 9, 9, 9]]))
]

report = code_execution(grids)
print(report)