import numpy as np
from typing import List

"""
The transformation identifies horizontal and vertical separators (lines of '6's)
in the input grid. Based on the separator configuration, it extracts subgrids
and rearranges them into the output grid following specific rules.

1.  Identify all horizontal rows (`h_seps`) and vertical columns (`v_seps`) composed entirely of '6'.
2.  Classify the configuration:
    a.  **Vertical Blocks**: Only `h_seps` exist.
    b.  **Horizontal Blocks**: Only `v_seps` exist.
    c.  **Quadrants**: Exactly one `h_sep` and one `v_sep` exist.
    d.  **Other**: Any other configuration (no separators, multiple crossing separators, etc.).
3.  Extract subgrids based on the configuration.
4.  Reassemble the output grid:
    a.  **Vertical Blocks Input**: Arrange subgrids horizontally, separated by vertical '6' columns. Input subgrids are ordered bottom-to-top, mapped to left-to-right in the output.
    b.  **Horizontal Blocks Input**: Arrange subgrids vertically, separated by horizontal '6' rows. Input subgrids are ordered left-to-right, mapped to top-to-bottom in the output.
    c.  **Quadrants Input**: Arrange the four quadrants (Top-Left (TL), Top-Right (TR), Bottom-Left (BL), Bottom-Right (BR)) vertically, separated by horizontal '6' rows, in the specific order: TL, BR, TR, BL.
    d.  **Other**: Return the input grid unchanged (based on lack of examples for other cases).
"""


def find_horizontal_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of rows composed entirely of 6s."""
    rows, _ = grid.shape
    separator_rows = []
    for r in range(rows):
        if np.all(grid[r, :] == 6):
            separator_rows.append(r)
    return separator_rows

def find_vertical_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of columns composed entirely of 6s."""
    _, cols = grid.shape
    separator_cols = []
    for c in range(cols):
        if np.all(grid[:, c] == 6):
            separator_cols.append(c)
    return separator_cols

def extract_vertical_blocks(grid: np.ndarray, h_seps: List[int]) -> List[np.ndarray]:
    """Extracts subgrids separated by horizontal lines. Returns top-to-bottom."""
    subgrids = []
    rows, _ = grid.shape
    row_indices = [-1] + sorted(h_seps) + [rows] # Ensure separators are sorted
    for r_idx in range(len(row_indices) - 1):
        start_row = row_indices[r_idx] + 1
        end_row = row_indices[r_idx + 1]
        if start_row < end_row: # Check for non-empty slice
            subgrid = grid[start_row:end_row, :]
            if subgrid.size > 0:
                subgrids.append(subgrid)
    return subgrids

def extract_horizontal_blocks(grid: np.ndarray, v_seps: List[int]) -> List[np.ndarray]:
    """Extracts subgrids separated by vertical lines. Returns left-to-right."""
    subgrids = []
    _, cols = grid.shape
    col_indices = [-1] + sorted(v_seps) + [cols] # Ensure separators are sorted
    for c_idx in range(len(col_indices) - 1):
        start_col = col_indices[c_idx] + 1
        end_col = col_indices[c_idx + 1]
        if start_col < end_col: # Check for non-empty slice
            subgrid = grid[:, start_col:end_col]
            if subgrid.size > 0:
                subgrids.append(subgrid)
    return subgrids

def assemble_horizontal_output(subgrids: List[np.ndarray]) -> np.ndarray:
    """Assembles subgrids horizontally (reversed input order), separated by vertical '6' columns."""
    if not subgrids:
        return np.array([[]], dtype=int)

    # Ensure all subgrids have the same height for hstack
    height = subgrids[0].shape[0]
    if not all(sg.shape[0] == height for sg in subgrids):
        # This case shouldn't happen with valid inputs based on examples
        # If it could, would need error handling or resizing logic
        raise ValueError("Subgrids must have the same height for horizontal assembly.")

    separator_col = np.full((height, 1), 6, dtype=int)
    output_parts = []

    # Reverse the order of subgrids (input bottom-to-top -> output left-to-right)
    reversed_subgrids = subgrids[::-1]

    for i, subgrid in enumerate(reversed_subgrids):
        output_parts.append(subgrid)
        if i < len(reversed_subgrids) - 1:
            output_parts.append(separator_col)

    if not output_parts: # Handle empty input case
         return np.array([[]], dtype=int)

    return np.hstack(output_parts)

def assemble_vertical_output(subgrids: List[np.ndarray]) -> np.ndarray:
    """Assembles subgrids vertically (original input order), separated by horizontal '6' rows."""
    if not subgrids:
        return np.array([[]], dtype=int)

     # Ensure all subgrids have the same width for vstack
    width = subgrids[0].shape[1]
    if not all(sg.shape[1] == width for sg in subgrids):
         # This case shouldn't happen with valid inputs based on examples
         raise ValueError("Subgrids must have the same width for vertical assembly.")

    separator_row = np.full((1, width), 6, dtype=int)
    output_parts = []

    # Use original order (input left-to-right -> output top-to-bottom)
    for i, subgrid in enumerate(subgrids):
        output_parts.append(subgrid)
        if i < len(subgrids) - 1:
            output_parts.append(separator_row)

    if not output_parts: # Handle empty input case
         return np.array([[]], dtype=int)

    return np.vstack(output_parts)


def assemble_quadrants_output(tl: np.ndarray, tr: np.ndarray, bl: np.ndarray, br: np.ndarray) -> np.ndarray:
    """Assembles quadrants vertically in specific order, separated by horizontal '6' rows."""
    # Basic check: Ensure quadrants have compatible widths for stacking
    if not (tl.shape[1] == tr.shape[1] == bl.shape[1] == br.shape[1]):
         raise ValueError("Quadrants must have the same width for vertical assembly.")

    width = tl.shape[1] # Assume all have same width
    separator_row = np.full((1, width), 6, dtype=int)

    # Order: Top-Left, Bottom-Right, Top-Right, Bottom-Left
    ordered_quadrants = [tl, br, tr, bl]
    output_parts = []

    for i, quadrant in enumerate(ordered_quadrants):
         # Only add non-empty quadrants (handles edge cases if separators are at borders)
        if quadrant.size > 0:
            if output_parts: # Add separator before adding the next quadrant
                output_parts.append(separator_row)
            output_parts.append(quadrant)

    if not output_parts: # Handle case where all quadrants might be empty
        return np.array([[]], dtype=int)

    return np.vstack(output_parts)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return [] # Handle empty input grid
    rows, cols = grid.shape

    # Find separators
    h_seps = find_horizontal_separators(grid)
    v_seps = find_vertical_separators(grid)

    output_grid_np = None

    # Determine configuration and apply transformation
    if h_seps and not v_seps:
        # Case: Vertical Blocks Input -> Horizontal Output
        subgrids = extract_vertical_blocks(grid, h_seps)
        if subgrids:
            output_grid_np = assemble_horizontal_output(subgrids)
        else: # No valid subgrids extracted
             output_grid_np = np.array([[]], dtype=int)

    elif v_seps and not h_seps:
        # Case: Horizontal Blocks Input -> Vertical Output
        subgrids = extract_horizontal_blocks(grid, v_seps)
        if subgrids:
             output_grid_np = assemble_vertical_output(subgrids)
        else: # No valid subgrids extracted
             output_grid_np = np.array([[]], dtype=int)

    elif len(h_seps) == 1 and len(v_seps) == 1:
        # Case: Quadrants Input -> Specific Vertical Output
        h_sep = h_seps[0]
        v_sep = v_seps[0]

        # Extract the four quadrants explicitly
        tl = grid[0:h_sep, 0:v_sep]
        tr = grid[0:h_sep, v_sep+1:cols]
        bl = grid[h_sep+1:rows, 0:v_sep]
        br = grid[h_sep+1:rows, v_sep+1:cols]

        # Check if all quadrants were intended (i.e., separators not at edges creating fewer than 4 regions)
        # The assembly function handles potentially empty quadrants from edge separators
        output_grid_np = assemble_quadrants_output(tl, tr, bl, br)

    else:
        # Case: Other (no separators, multiple crossing, etc.) - Return input
        # This handles cases not covered by the specific examples provided.
        output_grid_np = grid

    # Convert back to list of lists
    if output_grid_np is None or output_grid_np.size == 0:
         return [] # Return empty list if output is empty
    output_grid = output_grid_np.tolist()
    return output_grid