```python
import numpy as np

"""
Identifies patterns within three distinct 4x4 subgrids of the 4x14 input grid and maps each pattern to a specific color to construct rows of a 3x3 output grid.

1. Divide the 4x14 input grid into three 4x4 subgrids located at columns 0-3, 5-8, and 10-13.
2. For each subgrid (left to right):
    a. Identify the pattern formed by white (0) pixels against the gray (5) background. The possible patterns are:
        i. All Gray: Only gray (5) pixels.
        ii. Center Square: A 2x2 white (0) square at relative rows 1-2, cols 1-2.
        iii. Bottom Square: A 2x2 white (0) square at relative rows 2-3, cols 1-2.
        iv. Vertical Lines: Two 2-pixel vertical white (0) lines at relative rows 1-2, cols 0 and 3.
    b. Map the identified pattern to an output color:
        - All Gray -> Red (2)
        - Center Square -> Azure (8)
        - Bottom Square -> Yellow (4)
        - Vertical Lines -> Green (3)
3. Create a 3x3 output grid.
4. Fill each row `i` (0, 1, 2) of the output grid with the color determined from subgrid `i+1`.
"""

def _identify_pattern(subgrid: np.ndarray) -> str:
    """
    Identifies the specific pattern within a 4x4 subgrid.

    Args:
        subgrid: A 4x4 numpy array representing the subgrid.

    Returns:
        A string identifying the pattern ("center_square", "bottom_square",
        "vertical_lines", "all_gray", or "unknown").
    """
    # Define expected white pixel locations for each pattern (relative 0-based indices)
    patterns = {
        "center_square": [(1, 1), (1, 2), (2, 1), (2, 2)],
        "bottom_square": [(2, 1), (2, 2), (3, 1), (3, 2)],
        "vertical_lines": [(1, 0), (2, 0), (1, 3), (2, 3)],
    }
    
    rows, cols = subgrid.shape
    if rows != 4 or cols != 4:
         raise ValueError("Subgrid must be 4x4")

    # Check for specific non-gray patterns first
    for name, white_coords in patterns.items():
        is_match = True
        found_white_pixels = 0
        total_pixels = rows * cols
        
        # Check if all expected white pixels are white (0)
        for r, c in white_coords:
            if subgrid[r, c] != 0:
                is_match = False
                break
        if not is_match:
            continue # Try next pattern

        # Check if all *other* pixels are gray (5)
        for r in range(rows):
            for c in range(cols):
                if (r, c) in white_coords:
                     if subgrid[r, c] == 0:
                         found_white_pixels += 1
                     else: # Should not happen if first check passed
                         is_match = False
                         break
                elif subgrid[r, c] != 5:
                    is_match = False
                    break
            if not is_match:
                break
        
        # Final check: ensure correct number of white pixels and all others are gray
        if is_match and found_white_pixels == len(white_coords):
            return name

    # If no specific pattern matched, check if it's all gray
    if np.all(subgrid == 5):
        return "all_gray"

    # If none of the above, return unknown
    return "unknown"


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on identified patterns in subgrids.

    Args:
        input_grid: A 4x14 grid represented as a list of lists of integers.

    Returns:
        A 3x3 grid represented as a list of lists of integers.
    """
    input_np = np.array(input_grid, dtype=int)
    output_colors = []

    # Define subgrid column ranges (exclusive end index)
    subgrid_cols = [(0, 4), (5, 9), (10, 14)]

    # --- Workflow ---
    # 1. Iterate through the defined column ranges to extract subgrids
    for start_col, end_col in subgrid_cols:
        # 2. Extract the 4x4 subgrid
        subgrid = input_np[:, start_col:end_col]

        # 3. Identify the pattern within the subgrid
        pattern = _identify_pattern(subgrid)

        # 4. Map the identified pattern to the corresponding output color
        if pattern == "all_gray":
            output_colors.append(2) # red
        elif pattern == "center_square":
            output_colors.append(8) # azure
        elif pattern == "bottom_square":
            output_colors.append(4) # yellow
        elif pattern == "vertical_lines":
            output_colors.append(3) # green
        else:
             # Raise an error if an unrecognized pattern is found
             raise ValueError(f"Unknown or invalid pattern found in subgrid columns {start_col}-{end_col-1}")

    # 5. Construct the 3x3 output grid
    output_grid_size = 3
    output_grid = np.zeros((output_grid_size, output_grid_size), dtype=int)

    # 6. Fill each row of the output grid with the determined color
    if len(output_colors) != output_grid_size:
         raise ValueError(f"Expected {output_grid_size} output colors, but found {len(output_colors)}")
         
    for i, color in enumerate(output_colors):
        output_grid[i, :] = color

    # 7. Return the output grid as a list of lists
    return output_grid.tolist()
```