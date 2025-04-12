import numpy as np

"""
Identify rows and columns in the input grid that consist entirely of red (2) pixels. 
Create an output grid of the same dimensions, initialized to white (0). 
Fill the corresponding rows in the output grid with red (2) if they were fully red in the input. 
Fill the corresponding columns in the output grid with red (2) if they were fully red in the input.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by highlighting fully red rows and columns.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions as input_grid, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # Identify fully red rows
    fully_red_rows = []
    for r in range(height):
        # Check if all pixels in the row are red (2)
        if np.all(input_np[r, :] == 2):
            fully_red_rows.append(r)

    # Identify fully red columns
    fully_red_columns = []
    for c in range(width):
        # Check if all pixels in the column are red (2)
        if np.all(input_np[:, c] == 2):
            fully_red_columns.append(c)

    # Fill the identified fully red rows in the output grid
    for r in fully_red_rows:
        output_grid[r, :] = 2

    # Fill the identified fully red columns in the output grid
    for c in fully_red_columns:
        output_grid[:, c] = 2

    # Convert the numpy array back to a list of lists for the return type
    return output_grid.tolist()