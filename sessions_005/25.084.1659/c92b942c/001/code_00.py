import numpy as np

"""
Transforms an input grid by tiling it 3x3 and then adding blue (1) pixels horizontally adjacent and green (3) pixels diagonally adjacent to each non-white pixel from the original tiled pattern, only if the target adjacent cell is currently white (0).

1. Calculate the output grid dimensions (3 times the input height and width).
2. Create an initial output grid by tiling the input grid 3x3.
3. Create a final output grid, initially a copy of the tiled grid.
4. Iterate through each cell (R, C) of the tiled grid.
5. If the cell (R, C) in the tiled grid is non-white:
    a. Define relative coordinates for horizontal neighbors [(0, -1), (0, 1)] and diagonal neighbors [(-1, -1), (-1, 1), (1, -1), (1, 1)].
    b. For each horizontal neighbor:
        i. Calculate absolute coordinates (nR, nC).
        ii. Check if (nR, nC) is within the output grid boundaries.
        iii. Check if the cell (nR, nC) in the *final* output grid is white (0).
        iv. If both checks pass, set the cell (nR, nC) in the final output grid to blue (1).
    c. For each diagonal neighbor:
        i. Calculate absolute coordinates (nR, nC).
        ii. Check if (nR, nC) is within the output grid boundaries.
        iii. Check if the cell (nR, nC) in the *final* output grid is white (0).
        iv. If both checks pass, set the cell (nR, nC) in the final output grid to green (3).
6. Return the final output grid.
"""

def transform(input_grid):
    """
    Applies the tiling and enhancement transformation to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    H_in, W_in = input_np.shape
    H_out, W_out = H_in * 3, W_in * 3

    # Step 2: Create the initial tiled grid
    tiled_grid = np.tile(input_np, (3, 3))

    # Step 3: Create the final output grid as a copy
    output_grid = tiled_grid.copy()

    # Define relative neighbor coordinates and their corresponding colors
    horizontal_neighbors = [(0, -1), (0, 1)]
    diagonal_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    blue_color = 1
    green_color = 3

    # Step 4 & 5: Iterate through the tiled grid and apply enhancements
    for R in range(H_out):
        for C in range(W_out):
            # Check if the pixel in the *original* tiled grid was non-white
            if tiled_grid[R, C] != 0:
                # Check horizontal neighbors
                for dr, dc in horizontal_neighbors:
                    nR, nC = R + dr, C + dc
                    # Check boundaries and if the target cell in the *output* grid is white
                    if 0 <= nR < H_out and 0 <= nC < W_out and output_grid[nR, nC] == 0:
                        output_grid[nR, nC] = blue_color

                # Check diagonal neighbors
                for dr, dc in diagonal_neighbors:
                    nR, nC = R + dr, C + dc
                    # Check boundaries and if the target cell in the *output* grid is white
                    if 0 <= nR < H_out and 0 <= nC < W_out and output_grid[nR, nC] == 0:
                        output_grid[nR, nC] = green_color

    # Step 6: Return the final output grid (converting back to list of lists)
    return output_grid.tolist()