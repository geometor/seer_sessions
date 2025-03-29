import copy
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules applied pixel by pixel, considering the original neighbors:
    1. Gray (5) pixels become Yellow (4).
    2. Orange (7) pixels become Gray (5) if they are orthogonally adjacent (up, down, left, or right) to at least one Gray (5) pixel in the original input grid.
    3. Orange (7) pixels remain Orange (7) if they are not orthogonally adjacent to any Gray (5) pixel in the original input grid.
    4. All other colored pixels remain unchanged.
    The transformation checks neighbors in the original input grid before making changes to the output grid.
    """
    # Convert input list of lists to numpy array for easier slicing and neighbor checking
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Create a deep copy of the input grid to modify
    # This ensures pixels not matching specific rules are preserved
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]

            # Rule 1: Gray (5) becomes Yellow (4)
            if pixel_color == 5:
                output_grid[r][c] = 4
            
            # Rule 2 & 3: Conditional change for Orange (7)
            elif pixel_color == 7:
                # Check orthogonal neighbors for Gray (5) in the original input grid
                has_gray_neighbor = False
                # Check Up
                if r > 0 and input_np[r-1, c] == 5:
                    has_gray_neighbor = True
                # Check Down
                if not has_gray_neighbor and r < height - 1 and input_np[r+1, c] == 5:
                    has_gray_neighbor = True
                # Check Left
                if not has_gray_neighbor and c > 0 and input_np[r, c-1] == 5:
                    has_gray_neighbor = True
                # Check Right
                if not has_gray_neighbor and c < width - 1 and input_np[r, c+1] == 5:
                    has_gray_neighbor = True

                # Apply transformation based on neighbor check
                if has_gray_neighbor:
                    output_grid[r][c] = 5  # Change to Gray (5)
                else:
                    # If no gray neighbor, it remains Orange (7), which is already the case
                    # due to the deepcopy, so no explicit action needed here.
                    # output_grid[r][c] = 7 # Explicitly stating for clarity
                    pass

            # Rule 4: Other colors remain unchanged (handled by deepcopy)

    # Return the transformed grid (list of lists format)
    return output_grid