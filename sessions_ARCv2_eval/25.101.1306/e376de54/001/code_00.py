import numpy as np
from typing import List, Set, Tuple

"""
Identify the unique non-background colors present in the input grid.
Apply a specific transformation rule based on the exact set of colors found:

Rule 1 (Colors: Red(2), Maroon(9), Blue(1)):
- For each Red pixel, trace diagonally up-left and color any Orange(7) background pixels Red until a non-Orange pixel or grid boundary is hit.
- For each Maroon pixel, trace diagonally up-right and color any Orange(7) background pixels Maroon until a non-Orange pixel or grid boundary is hit.
- For each Blue pixel, trace diagonally down-right and color any Orange(7) background pixels Blue until a non-Orange pixel or grid boundary is hit.

Rule 2 (Colors: Gray(5), Maroon(9), Green(3)):
- For each row, identify contiguous horizontal segments of Gray, Maroon, or Green.
- Extend each segment rightwards to end at column index 9 (inclusive) by changing Orange(7) pixels to the segment's color.
- Truncate each segment that extends beyond column index 9 by changing pixels from column index 10 onwards back to Orange(7).

Rule 3 (Color: Azure(8)):
- For each column, find all Azure pixels.
- If there are two or more Azure pixels in a column, consider pairs of vertically adjacent Azure pixels.
- If the space between a pair of vertically adjacent Azure pixels consists entirely of Orange(7) background pixels, fill that space with Azure(8).

If none of these exact color sets are found, return the input grid unchanged.
The background color is assumed to be Orange(7).
"""

def get_unique_colors(grid: np.ndarray, background_color: int = 7) -> Set[int]:
    """Finds unique colors in the grid, excluding the background color."""
    unique_colors = set(np.unique(grid))
    unique_colors.discard(background_color)
    return unique_colors

def apply_rule_1(input_grid: np.ndarray, output_grid: np.ndarray, height: int, width: int):
    """Applies diagonal extension rule for Red, Maroon, Blue."""
    background_color = 7
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            
            # Red (2): Trace up-left
            if color == 2:
                for i in range(1, max(height, width)):
                    nr, nc = r - i, c - i
                    if not (0 <= nr < height and 0 <= nc < width):
                        break
                    if input_grid[nr, nc] == background_color:
                        output_grid[nr, nc] = 2
                    else:
                        break # Stop tracing if non-background hit
                        
            # Maroon (9): Trace up-right
            elif color == 9:
                 for i in range(1, max(height, width)):
                    nr, nc = r - i, c + i
                    if not (0 <= nr < height and 0 <= nc < width):
                        break
                    if input_grid[nr, nc] == background_color:
                        output_grid[nr, nc] = 9
                    else:
                        break # Stop tracing if non-background hit

            # Blue (1): Trace down-right
            elif color == 1:
                for i in range(1, max(height, width)):
                    nr, nc = r + i, c + i
                    if not (0 <= nr < height and 0 <= nc < width):
                        break
                    if input_grid[nr, nc] == background_color:
                        output_grid[nr, nc] = 1
                    else:
                        break # Stop tracing if non-background hit

def apply_rule_2(input_grid: np.ndarray, output_grid: np.ndarray, height: int, width: int):
    """Applies horizontal adjustment rule for Gray, Maroon, Green to column 9."""
    target_col_index = 9
    background_color = 7
    rule_colors = {5, 9, 3}

    for r in range(height):
        c = 0
        while c < width:
            color = input_grid[r, c]
            if color in rule_colors:
                # Find the end of the segment
                c_start = c
                c_end = c
                while c_end + 1 < width and input_grid[r, c_end + 1] == color:
                    c_end += 1
                
                # Apply extension/truncation logic
                # Extend if segment ends before target column
                if c_end < target_col_index:
                    for fill_c in range(c_end + 1, target_col_index + 1):
                         if fill_c < width: # Check bounds before filling
                             output_grid[r, fill_c] = color
                             
                # Truncate if segment ends after target column
                # Note: We only need to clear *beyond* the target column index
                if c_end > target_col_index:
                    for clear_c in range(target_col_index + 1, c_end + 1):
                         if clear_c < width: # Check bounds before clearing
                            output_grid[r, clear_c] = background_color

                # Move past the processed segment
                c = c_end + 1
            else:
                c += 1


def apply_rule_3(input_grid: np.ndarray, output_grid: np.ndarray, height: int, width: int):
    """Applies vertical gap filling rule for Azure."""
    color_to_fill = 8
    background_color = 7

    for c in range(width):
        azure_rows = [r for r in range(height) if input_grid[r, c] == color_to_fill]
        
        if len(azure_rows) >= 2:
            # Sort rows just in case, though find iteration should preserve order
            azure_rows.sort() 
            
            for i in range(len(azure_rows) - 1):
                r1 = azure_rows[i]
                r2 = azure_rows[i+1]
                
                # Check if there's a gap between them
                if r2 > r1 + 1:
                    # Check if the gap is entirely background color
                    is_background_gap = True
                    for r_gap in range(r1 + 1, r2):
                        if input_grid[r_gap, c] != background_color:
                            is_background_gap = False
                            break
                    
                    # If it's a pure background gap, fill it
                    if is_background_gap:
                        for r_fill in range(r1 + 1, r2):
                            output_grid[r_fill, c] = color_to_fill


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the set of unique non-background colors present.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = input_np.copy()
    height, width = input_np.shape
    background_color = 7

    # Identify the unique colors present (excluding background)
    unique_colors = get_unique_colors(input_np, background_color)

    # --- Conditional Rule Application ---

    # Rule 1 condition: Exactly Red(2), Maroon(9), Blue(1)
    if unique_colors == {1, 2, 9}:
        apply_rule_1(input_np, output_np, height, width)
        
    # Rule 2 condition: Exactly Gray(5), Maroon(9), Green(3)
    elif unique_colors == {3, 5, 9}:
        apply_rule_2(input_np, output_np, height, width)
        
    # Rule 3 condition: Exactly Azure(8)
    elif unique_colors == {8}:
        apply_rule_3(input_np, output_np, height, width)
        
    # Else: No specific rule matches the color set, output remains a copy of input.

    # Convert back to list of lists for the expected output format
    return output_np.tolist()