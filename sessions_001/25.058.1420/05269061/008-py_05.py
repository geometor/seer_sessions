"""
1.  **Identify Seed Size:** The seed size corresponds to the repeating unit size in the input grid. Examine the input grid. Count the number of columns until the first non-zero number repeats, this is the dimension of the square seed.
2.  **Extract Seed:** Create an empty square matrix filled with zeros with dimensions obtained in previous step.
3.  **Populate seed:** Iterate through the non-zero elements of the input's first row. For each element, place the value into the dynamic seed at the row index corresponding to its position in the sequence, starting from 0.
4.  **Tile the Seed:** Tile the created seed across the output grid, repeating it both horizontally and vertically to match the dimensions of the input grid. The output grid's dimensions will be the same size of the input grid.
"""

import numpy as np

def get_seed_size(grid):
    """Determines the seed size based on the repeating pattern in the first row."""
    first_row = grid[0]
    non_zero_indices = np.where(first_row != 0)[0]
    if len(non_zero_indices) < 2:
        return len(first_row)  # Handle cases with fewer than 2 non-zero elements
    return non_zero_indices[1]

def create_seed(size, first_row):
    """Creates the seed matrix and populates it based on the first row's non-zero elements."""
    seed = np.zeros((size, size), dtype=int)
    non_zero_elements = first_row[first_row != 0]
    for i, value in enumerate(non_zero_elements):
        seed[i % size, i % size] = value # correct diagonal placement.
        
        #find next available 0 from left to right in that row
        for j in range(size):
             if seed[i % size, j] == 0:
                seed[i % size, j] = value
                break

    return seed

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Seed Size.
    seed_size = get_seed_size(input_grid)

    # 2. Extract Seed.
    seed = create_seed(seed_size, input_grid[0])

    # 3. Tile the Seed.
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = seed[i % seed_size, j % seed_size]

    return output_grid.tolist()