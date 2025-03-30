```python
import numpy as np
from collections import Counter
import math

"""
The transformation rule involves identifying a repeating background pattern in the input grid that is partially obscured by noise (pixels of color blue, value 1). The goal is to remove the noise and restore the underlying pattern across the entire grid.

1.  **Identify Noise:** The noise color is blue (1).
2.  **Determine Pattern Dimensions:** Find the height (H) and width (W) of the smallest repeating unit (tile) of the background pattern. This is done by analyzing the periodicity of rows and columns, ignoring the noise pixels. The smallest H > 0 is found such that for all rows r >= H, row r is consistent with row r % H (ignoring noise). Similarly, the smallest W > 0 is found such that for all columns c >= W, column c is consistent with column c % W (ignoring noise).
3.  **Infer Base Pattern Tile:** Create an HxW tile representing the fundamental repeating unit. For each position (ph, pw) within this tile (0 <= ph < H, 0 <= pw < W):
    a.  Gather all pixel values from the input grid at locations (r, c) where r % H == ph and c % W == pw.
    b.  Filter out the noise color (1) from the gathered pixels.
    c.  If only noise pixels were found for this position, the pattern color for (ph, pw) is the noise color (1).
    d.  Otherwise, determine the most frequent color among the non-noise pixels gathered for this position. This color becomes the pattern color for (ph, pw).
4.  **Reconstruct Output Grid:** Create an output grid of the same dimensions as the input grid. Fill each cell (r, c) of the output grid with the color from the inferred base pattern tile at position (r % H, c % W).
"""

def find_pattern_dimensions(grid: np.ndarray, noise_color: int = 1) -> tuple[int, int]:
    """
    Determines the height (H) and width (W) of the repeating pattern tile.

    Args:
        grid: The input grid as a numpy array.
        noise_color: The integer value representing noise pixels to ignore.

    Returns:
        A tuple (H, W) representing the pattern dimensions.
    """
    grid_height, grid_width = grid.shape
    H = grid_height
    W = grid_width

    # Find smallest repeating height H
    for h_candidate in range(1, grid_height):
        is_periodic_height = True
        # Check if rows repeat with period h_candidate, ignoring noise
        for r in range(h_candidate, grid_height):
            for c in range(grid_width):
                val1 = grid[r, c]
                val2 = grid[r - h_candidate, c] # Compare with row H positions above
                # Check for mismatch only if neither is noise
                if val1 != noise_color and val2 != noise_color and val1 != val2:
                    is_periodic_height = False
                    break
            if not is_periodic_height:
                break
        
        # Check consistency using modulo - rows r and r % H should match where not noise
        is_consistent_mod = True
        if is_periodic_height: # Optional secondary check for robustness
             for r in range(h_candidate, grid_height):
                 for c in range(grid_width):
                     val1 = grid[r, c]
                     val2 = grid[r % h_candidate, c]
                     if val1 != noise_color and val2 != noise_color and val1 != val2:
                        is_consistent_mod = False
                        break
                 if not is_consistent_mod:
                    break
        
        # If both checks (or just the first one if preferred) pass, we found H
        # Using the first check (periodicity) as primary.
        if is_periodic_height: # and is_consistent_mod: 
            H = h_candidate
            break

    # Find smallest repeating width W
    for w_candidate in range(1, grid_width):
        is_periodic_width = True
        # Check if columns repeat with period w_candidate, ignoring noise
        for c in range(w_candidate, grid_width):
            for r in range(grid_height):
                val1 = grid[r, c]
                val2 = grid[r, c - w_candidate] # Compare with column W positions left
                # Check for mismatch only if neither is noise
                if val1 != noise_color and val2 != noise_color and val1 != val2:
                    is_periodic_width = False
                    break
            if not is_periodic_width:
                break
        
        # Check consistency using modulo
        is_consistent_mod = True
        if is_periodic_width:
            for c in range(w_candidate, grid_width):
                for r in range(grid_height):
                    val1 = grid[r, c]
                    val2 = grid[r, c % w_candidate]
                    if val1 != noise_color and val2 != noise_color and val1 != val2:
                        is_consistent_mod = False
                        break
                if not is_consistent_mod:
                    break

        if is_periodic_width: # and is_consistent_mod:
            W = w_candidate
            break
            
    # Fallback if no period found (shouldn't happen with task structure)
    if H == grid_height and W == grid_width:
         print(f"Warning: Could not determine clear periodicity. Using full grid dimensions ({grid_height}x{grid_width}).")


    return H, W


def infer_pattern_tile(grid: np.ndarray, H: int, W: int, noise_color: int = 1) -> np.ndarray:
    """
    Infers the HxW base pattern tile from the noisy grid.

    Args:
        grid: The input grid as a numpy array.
        H: The height of the pattern tile.
        W: The width of the pattern tile.
        noise_color: The integer value representing noise pixels.

    Returns:
        An HxW numpy array representing the base pattern tile.
    """
    pattern_tile = np.zeros((H, W), dtype=int)
    grid_height, grid_width = grid.shape

    for ph in range(H):
        for pw in range(W):
            # Collect all pixels in the input grid corresponding to this pattern tile position
            pixels = []
            # Iterate through all grid cells that map to (ph, pw) in the tile structure
            for r in range(ph, grid_height, H):
                 for c in range(pw, grid_width, W):
                    pixels.append(grid[r,c])

            # Filter out the noise color
            non_noise_pixels = [p for p in pixels if p != noise_color]

            # Determine the pattern color for this position
            if not non_noise_pixels:
                # If only noise pixels were found, the pattern color is the noise color
                pattern_tile[ph, pw] = noise_color
            else:
                # Otherwise, find the most frequent non-noise color
                count = Counter(non_noise_pixels)
                # most_common returns list of (element, count) tuples
                most_common_color = count.most_common(1)[0][0]
                pattern_tile[ph, pw] = most_common_color

    return pattern_tile


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Restores a repeating background pattern in a grid obscured by noise (blue=1).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the restored grid.
    """
    # Convert input to numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    grid_height, grid_width = input_array.shape
    noise_color = 1 # Blue is the noise color in the examples

    # Step 1: Determine the dimensions (H, W) of the repeating pattern tile
    # We refine the dimension finding logic here. Instead of simple periodicity,
    # let's find the smallest H, W such that the grid *mostly* conforms
    # to grid[r,c] == grid[r % H, c % W] when not noise.
    # Using the previously defined function, which checks periodicity.
    H, W = find_pattern_dimensions(input_array, noise_color)
    #print(f"Determined Pattern Dimensions: H={H}, W={W}") # Debug print

    # Step 2: Infer the HxW base pattern tile by finding the mode color for each position
    pattern_tile = infer_pattern_tile(input_array, H, W, noise_color)
    #print("Inferred Pattern Tile:") # Debug print
    #print(pattern_tile) # Debug print


    # Step 3: Create the output grid by tiling the inferred pattern
    output_array = np.zeros_like(input_array)
    for r in range(grid_height):
        for c in range(grid_width):
            # Use the modulo operator to find the corresponding position in the pattern tile
            pattern_row = r % H
            pattern_col = c % W
            output_array[r, c] = pattern_tile[pattern_row, pattern_col]

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```