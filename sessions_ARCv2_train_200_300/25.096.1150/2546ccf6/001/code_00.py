import numpy as np
from collections import Counter

"""
The transformation identifies a 3x3 grid structure defined by separator lines of a single color.
It then performs conditional copying of sections based on the content color of the central section (1,1).

1.  Copy the input grid to the output grid.
2.  Identify the separator color and the row/column indices defining the 9 sections.
3.  Extract the content of the middle-middle section (1,1) from the input.
4.  Identify the primary content color (non-zero, non-separator) within the middle-middle section.
5.  Copy the content of the input middle-middle section (1,1) to the output top-middle section (0,1).
6.  Extract the content and primary color of the input middle-left section (1,0).
7.  If the primary color of the middle-left section matches the primary color of the middle-middle section (and the middle-middle color exists), copy the content of the input middle-left section (1,0) to the output top-left section (0,0).
8.  Extract the content and primary color of the input bottom-middle section (2,1).
9.  If the primary color of the bottom-middle section matches the primary color of the middle-middle section (and the middle-middle color exists), copy the content of the input bottom-middle section (2,1) to the output bottom-left section (2,0).
10. Return the modified output grid.
"""


def _find_separators(grid_np: np.ndarray) -> tuple[int, list[int], list[int]]:
    """Finds the separator color and the indices of separator rows/columns."""
    sep_color = 0
    sep_rows = []
    sep_cols = []
    rows, cols = grid_np.shape

    # Find horizontal separators
    for r in range(rows):
        first_val = grid_np[r, 0]
        if first_val != 0 and np.all(grid_np[r, :] == first_val):
            sep_rows.append(r)
            if sep_color == 0:
                sep_color = first_val
            elif sep_color != first_val:
                 # This case should ideally not happen based on examples
                 # If it does, the logic might need refinement.
                 # For now, we stick with the first found color.
                 pass

    # Find vertical separators
    for c in range(cols):
        first_val = grid_np[0, c]
        if first_val != 0 and np.all(grid_np[:, c] == first_val):
            sep_cols.append(c)
            if sep_color == 0:
                sep_color = first_val
            elif sep_color != first_val:
                # As above, handle potential inconsistencies if needed.
                pass
    
    # Basic validation - expect 2 separator lines each way
    if len(sep_rows) != 2 or len(sep_cols) != 2:
        # Fallback or raise error if grid structure is unexpected
        # For now, proceed assuming the structure holds for valid inputs
        pass
        
    return sep_color, sorted(sep_rows), sorted(sep_cols)

def _get_section_bounds(grid_shape: tuple[int, int], sep_rows: list[int], sep_cols: list[int]) -> tuple[list[int], list[int]]:
    """Calculates the start/end boundaries for rows and columns of the 9 sections."""
    rows, cols = grid_shape
    row_bounds = [0] + sep_rows + [rows]
    col_bounds = [0] + sep_cols + [cols]
    # Adjust bounds to exclude the separator lines themselves from the section content
    # Section row starts after previous separator, ends before next separator
    # Section col starts after previous separator, ends before next separator
    adjusted_row_bounds = [row_bounds[0], row_bounds[1]+1, row_bounds[2]+1]
    adjusted_row_ends = [sep_rows[0], sep_rows[1], row_bounds[3]]
    adjusted_col_bounds = [col_bounds[0], col_bounds[1]+1, col_bounds[2]+1]
    adjusted_col_ends = [sep_cols[0], sep_cols[1], col_bounds[3]]
    
    # Return pairs of (start, end) for rows and columns
    final_row_bounds = [(adjusted_row_bounds[i], adjusted_row_ends[i]) for i in range(3)]
    final_col_bounds = [(adjusted_col_bounds[i], adjusted_col_ends[i]) for i in range(3)]

    return final_row_bounds, final_col_bounds


def _get_section(grid_np: np.ndarray, r_idx: int, c_idx: int, row_bounds: list[tuple[int, int]], col_bounds: list[tuple[int, int]]) -> np.ndarray:
    """Extracts the content of a specific section."""
    r_start, r_end = row_bounds[r_idx]
    c_start, c_end = col_bounds[c_idx]
    return grid_np[r_start:r_end, c_start:c_end]

def _set_section(grid_np: np.ndarray, r_idx: int, c_idx: int, row_bounds: list[tuple[int, int]], col_bounds: list[tuple[int, int]], content: np.ndarray):
    """Sets the content of a specific section."""
    r_start, r_end = row_bounds[r_idx]
    c_start, c_end = col_bounds[c_idx]
    
    # Ensure content dimensions match section dimensions
    expected_shape = (r_end - r_start, c_end - c_start)
    if content.shape == expected_shape:
        grid_np[r_start:r_end, c_start:c_end] = content
    else:
        # Handle dimension mismatch - this might indicate an error in boundary calculation or logic
        # For robustness, could try resizing/padding, but for now assume match
        print(f"Warning: Shape mismatch when setting section ({r_idx},{c_idx}). Expected {expected_shape}, got {content.shape}")
        # Attempt assignment anyway if broadcasting allows (e.g., single value fill)
        if content.size == 1:
             grid_np[r_start:r_end, c_start:c_end] = content.item()
        # else: # Or raise an error
        #     raise ValueError("Dimension mismatch in set_section")


def _get_primary_color(section: np.ndarray, sep_color: int) -> int | None:
    """Finds the single non-zero, non-separator color in the section."""
    unique_vals = np.unique(section)
    content_colors = [val for val in unique_vals if val != 0 and val != sep_color]
    
    if len(content_colors) == 1:
        return content_colors[0]
    # If zero or multiple content colors, return None (or handle ambiguity differently if needed)
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying a 3x3 structure based on separator lines
    and conditionally copying sections based on the color found in the central section.
    Specifically, copies middle-middle to top-middle, and conditionally copies
    middle-left to top-left and bottom-middle to bottom-left if their primary colors
    match the middle-middle section's primary color.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy()
    
    # Find separator lines and color
    sep_color, sep_rows, sep_cols = _find_separators(input_np)
    
    # If separators weren't found correctly, return the original grid
    if sep_color == 0 or len(sep_rows) != 2 or len(sep_cols) != 2:
         print("Warning: Could not reliably determine grid structure. Returning original grid.")
         return input_grid # Or output_np.tolist() if preferred

    # Determine section boundaries (excluding separators)
    row_bounds, col_bounds = _get_section_bounds(input_np.shape, sep_rows, sep_cols)

    # --- Core Logic ---
    
    # 1. Get Middle-Middle section (1, 1) content and primary color
    mid_mid_content = _get_section(input_np, 1, 1, row_bounds, col_bounds)
    mid_mid_color = _get_primary_color(mid_mid_content, sep_color)

    # 2. Copy Middle-Middle (1,1) content to Top-Middle (0,1) in output
    _set_section(output_np, 0, 1, row_bounds, col_bounds, mid_mid_content)

    # 3. Check Middle-Left section (1, 0)
    mid_left_content = _get_section(input_np, 1, 0, row_bounds, col_bounds)
    mid_left_color = _get_primary_color(mid_left_content, sep_color)

    # 4. Conditional copy Middle-Left (1,0) to Top-Left (0,0)
    if mid_mid_color is not None and mid_left_color == mid_mid_color:
        _set_section(output_np, 0, 0, row_bounds, col_bounds, mid_left_content)

    # 5. Check Bottom-Middle section (2, 1)
    bot_mid_content = _get_section(input_np, 2, 1, row_bounds, col_bounds)
    bot_mid_color = _get_primary_color(bot_mid_content, sep_color)

    # 6. Conditional copy Bottom-Middle (2,1) to Bottom-Left (2,0)
    if mid_mid_color is not None and bot_mid_color == mid_mid_color:
        _set_section(output_np, 2, 0, row_bounds, col_bounds, bot_mid_content)

    # Convert the result back to a list of lists
    return output_np.tolist()