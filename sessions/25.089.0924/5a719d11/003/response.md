```python
import numpy as np
from collections import Counter
import copy

"""
Transformation Rule:

1.  **Identify Separator:** Locate the central cross (one row, one column) composed entirely of white (0) pixels. This cross divides the grid into four quadrants.
2.  **Initialize Output:** Create a copy of the input grid.
3.  **Process Quadrants:** For each of the four quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right):
    a.  **Determine Background Color:** Find the non-white color of pixels *within* the quadrant that are directly adjacent (including diagonals) to any white pixel belonging to the separator cross. If multiple such colors exist, choose the most frequent one among them within the quadrant. If no non-white pixels are adjacent to the separator, use the most frequent non-white color within the entire quadrant as the background color. If the quadrant is entirely white, the background color is considered white (0).
    b.  **Replace Foreground Pixels:** Iterate through all pixels within the current quadrant in the *input* grid. If a pixel's color is not white (0) and not the determined background color for that quadrant, change the corresponding pixel in the *output* grid to the quadrant's background color.
4.  **Return:** The modified output grid. The white separator pixels and the background pixels remain unchanged.
"""

def find_separator(grid):
    """Finds the row and column index of the white (0) separator cross."""
    height, width = grid.shape
    sep_row, sep_col = -1, -1

    # Find separator row (all zeros)
    for r in range(height):
        if np.all(grid[r, :] == 0):
            sep_row = r
            break

    # Find separator column (all zeros)
    for c in range(width):
        if np.all(grid[:, c] == 0):
            sep_col = c
            break

    # Return -1 for indices if not found, though examples imply they exist.
    return sep_row, sep_col

def find_quadrant_background_color(grid, row_slice, col_slice, sep_row, sep_col):
    """
    Determines the background color of a quadrant based on adjacency to the separator.
    Fallback to most frequent if no adjacent or multiple adjacent colors.
    """
    height, width = grid.shape
    quadrant_view = grid[row_slice, col_slice]

    # Handle empty quadrants immediately
    if quadrant_view.size == 0:
        return 0

    adjacent_colors_pixels = [] # Store (color, r, c) for adjacent pixels

    # Iterate through pixels *within* the quadrant's slice definition
    for r_idx, r in enumerate(range(row_slice.start, row_slice.stop)):
        if r >= height: continue # Boundary check
        for c_idx, c in enumerate(range(col_slice.start, col_slice.stop)):
            if c >= width: continue # Boundary check

            pixel_color = grid[r, c]
            if pixel_color == 0: # Skip white pixels
                continue

            # Check if this pixel (r, c) is adjacent (8-connectivity) to the separator
            is_adjacent_to_separator = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue # Skip self
                    
                    nr, nc = r + dr, c + dc
                    
                    # Check if neighbor (nr, nc) is within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is part of the separator (is white AND on sep_row or sep_col)
                        if grid[nr, nc] == 0 and (nr == sep_row or nc == sep_col):
                            is_adjacent_to_separator = True
                            break # Found adjacent separator pixel
                if is_adjacent_to_separator:
                    break # Move to next pixel check

            if is_adjacent_to_separator:
                adjacent_colors_pixels.append(pixel_color)

    # Determine background color based on adjacent pixels found
    if len(adjacent_colors_pixels) > 0:
        # Count frequencies of colors found adjacent to the separator
        adjacent_counts = Counter(adjacent_colors_pixels)
        # Return the most frequent adjacent color
        background_color = adjacent_counts.most_common(1)[0][0]
        return background_color
    else:
        # Fallback: No non-white pixels adjacent to separator found.
        # Use the most frequent non-white color in the entire quadrant.
        all_quadrant_pixels = quadrant_view.flatten()
        non_zero_pixels = all_quadrant_pixels[all_quadrant_pixels != 0]
        
        if non_zero_pixels.size == 0:
            return 0 # Quadrant is all white
            
        counts = Counter(non_zero_pixels)
        if not counts: # Should not happen if non_zero_pixels exist
             return 0
        # Return the most frequent color within the quadrant
        # print(f"Debug: No adjacent colors found for quadrant {row_slice, col_slice}. Using most frequent overall.")
        background_color = counts.most_common(1)[0][0]
        return background_color


def transform(input_grid):
    """
    Applies the quadrant-based foreground pixel replacement rule.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Identify Separator
    sep_row, sep_col = find_separator(input_np)

    # Basic check if separator was found (essential for this logic)
    if sep_row == -1 or sep_col == -1:
         # If no separator, the logic doesn't apply. Return the original grid.
         # Consider adding a more robust error or alternative logic if needed.
         print("Warning: Separator cross not found. Returning input grid unchanged.")
         return input_grid # Return original list of lists

    # 2. Define Quadrant Slices
    quadrant_slices = [
        # Top-Left (TL)
        (slice(0, sep_row), slice(0, sep_col)),
        # Top-Right (TR)
        (slice(0, sep_row), slice(sep_col + 1, width)),
        # Bottom-Left (BL)
        (slice(sep_row + 1, height), slice(0, sep_col)),
        # Bottom-Right (BR)
        (slice(sep_row + 1, height), slice(sep_col + 1, width))
    ]

    # 3. Process Each Quadrant
    for row_slice, col_slice in quadrant_slices:
        
        # Check if the quadrant slice definition is valid (e.g., not zero size)
        if row_slice.start >= row_slice.stop or col_slice.start >= col_slice.stop:
            continue # Skip empty or invalid quadrants

        # a. Find Background Color for this quadrant using the adjacency rule
        background_color = find_quadrant_background_color(input_np, row_slice, col_slice, sep_row, sep_col)

        # If background is white (e.g., all-white quadrant), nothing to change within it
        if background_color == 0:
            continue

        # b. Identify and Replace Foreground Pixels within this quadrant's area in the output grid
        # Iterate through the indices defined by the slices
        for r in range(row_slice.start, row_slice.stop):
             # Check row index just in case stop goes out of bounds (shouldn't with np slicing)
            if r >= height: continue
            for c in range(col_slice.start, col_slice.stop):
                # Check col index just in case
                if c >= width: continue

                current_pixel_color = input_np[r, c]
                # Check if it's a foreground pixel (not white and not background)
                if current_pixel_color != 0 and current_pixel_color != background_color:
                    # Replace in the output grid
                    output_np[r, c] = background_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()

```