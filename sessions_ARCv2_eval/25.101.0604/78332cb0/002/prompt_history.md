
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

*   **Perception**: The task involves rearranging subgrids extracted from an input grid. The input grids contain subgrids separated by lines or columns composed entirely of the digit '6'. The arrangement of these separators (horizontal, vertical, or both) determines how the subgrids are extracted and how they are reassembled in the output. The reassembly involves changing the orientation (e.g., vertically stacked input blocks become horizontally arranged output blocks) and potentially the order of the blocks.

*   **Facts**:
    ```yaml
    task_type: grid_rearrangement
    components:
      - object: grid
        attributes:
          - type: input_grid
          - type: output_grid
          - content: matrix of digits
      - object: separator
        attributes:
          - value: 6
          - role: delimiter
          - type: horizontal_line (row of 6s)
          - type: vertical_column (column of 6s)
      - object: subgrid
        attributes:
          - content: portion of the input grid delimited by separators
          - role: element_to_be_rearranged
    relationships:
      - separators divide the input_grid into subgrids
      - subgrids from input_grid are assembled into output_grid
    actions:
      - identify_separators: Find horizontal lines and vertical columns of '6's in the input_grid.
      - split_grid: Divide the input_grid into subgrids based on the identified separators.
      - determine_arrangement: Classify the input arrangement based on separator orientation (vertical blocks, horizontal blocks, or quadrants).
      - reassemble_grid: Construct the output_grid by arranging the extracted subgrids according to specific rules based on the input arrangement.
        rules:
          - if input has horizontal separators only (vertical blocks):
              - arrange blocks horizontally in output
              - use vertical '6' columns as separators
              - reverse the order of blocks (bottom block first)
          - if input has vertical separators only (horizontal blocks):
              - arrange blocks vertically in output
              - use horizontal '6' lines as separators
              - preserve the order of blocks (left block first)
          - if input has central horizontal and vertical separators (quadrants):
              - arrange quadrants vertically in output
              - use horizontal '6' lines as separators
              - specific order: Top-Left, Bottom-Right, Top-Right, Bottom-Left
    ```

*   **Natural Language Program**:
    1.  Scan the input grid to locate all complete horizontal rows and complete vertical columns consisting solely of the digit '6'. These are the separators.
    2.  Analyze the configuration of separators:
        a.  **Vertical Blocks**: If only horizontal separator rows exist, they divide the grid into vertically stacked subgrids.
        b.  **Horizontal Blocks**: If only vertical separator columns exist, they divide the grid into horizontally arranged subgrids.
        c.  **Quadrants**: If a central horizontal row and a central vertical column of separators exist, they divide the grid into four quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
    3.  Extract the subgrids, excluding the separator lines/columns themselves.
    4.  Construct the output grid based on the identified configuration:
        a.  For **Vertical Blocks**: Arrange the extracted subgrids horizontally, placing the bottom-most input subgrid first (on the left), followed by the next subgrid up, and so on, ending with the top-most input subgrid (on the right). Separate adjacent subgrids in the output with a single vertical column of '6's.
        b.  For **Horizontal Blocks**: Arrange the extracted subgrids vertically, placing the left-most input subgrid first (at the top), followed by the next subgrid to its right, and so on, ending with the right-most input subgrid (at the bottom). Separate adjacent subgrids in the output with a single horizontal row of '6's.
        c.  For **Quadrants**: Arrange the extracted quadrants vertically in the specific order: Top-Left, Bottom-Right, Top-Right, Bottom-Left. Separate adjacent quadrants in the output with a single horizontal row of '6's.
```python
import numpy as np
from typing import List

"""
The transformation identifies horizontal and vertical separators (lines of '6's)
in the input grid. Based on the separator configuration, it extracts subgrids
and rearranges them into the output grid.

1.  **Identify Separators**: Find all full rows and columns composed solely of '6'.
2.  **Determine Configuration**:
    - If only horizontal separators exist -> Vertical Blocks.
    - If only vertical separators exist -> Horizontal Blocks.
    - If both a central horizontal and a central vertical separator exist -> Quadrants.
3.  **Extract Subgrids**: Split the grid based on separators.
4.  **Reassemble Output**:
    - **Vertical Blocks (Input)**: Arrange blocks horizontally in reverse order (bottom to top), separated by vertical '6' columns.
    - **Horizontal Blocks (Input)**: Arrange blocks vertically in original order (left to right), separated by horizontal '6' rows.
    - **Quadrants (Input)**: Arrange quadrants vertically in the order: Top-Left, Bottom-Right, Top-Right, Bottom-Left, separated by horizontal '6' rows.
"""

def find_horizontal_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of rows composed entirely of 6s."""
    rows, cols = grid.shape
    separator_rows = []
    for r in range(rows):
        if np.all(grid[r, :] == 6):
            separator_rows.append(r)
    return separator_rows

def find_vertical_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of columns composed entirely of 6s."""
    rows, cols = grid.shape
    separator_cols = []
    for c in range(cols):
        if np.all(grid[:, c] == 6):
            separator_cols.append(c)
    return separator_cols

def extract_subgrids(grid: np.ndarray, h_seps: List[int], v_seps: List[int]) -> List[np.ndarray]:
    """Extracts subgrids based on separator locations."""
    subgrids = []
    rows, cols = grid.shape

    row_indices = [-1] + h_seps + [rows]
    col_indices = [-1] + v_seps + [cols]

    for r_idx in range(len(row_indices) - 1):
        start_row = row_indices[r_idx] + 1
        end_row = row_indices[r_idx + 1]
        if start_row >= end_row: continue # Skip empty segments

        for c_idx in range(len(col_indices) - 1):
            start_col = col_indices[c_idx] + 1
            end_col = col_indices[c_idx + 1]
            if start_col >= end_col: continue # Skip empty segments

            subgrid = grid[start_row:end_row, start_col:end_col]
            if subgrid.size > 0: # Only add non-empty subgrids
                subgrids.append(subgrid)

    return subgrids

def assemble_horizontal_blocks(subgrids: List[np.ndarray]) -> np.ndarray:
    """Assembles subgrids vertically, separated by horizontal '6' rows."""
    if not subgrids:
        return np.array([[]], dtype=int)

    subgrid_height, subgrid_width = subgrids[0].shape
    separator_row = np.full((1, subgrid_width), 6, dtype=int)
    output_parts = []

    for i, subgrid in enumerate(subgrids):
        output_parts.append(subgrid)
        if i < len(subgrids) - 1:
            output_parts.append(separator_row)

    return np.vstack(output_parts)

def assemble_vertical_blocks(subgrids: List[np.ndarray]) -> np.ndarray:
    """Assembles subgrids horizontally (reversed order), separated by vertical '6' columns."""
    if not subgrids:
        return np.array([[]], dtype=int)

    subgrid_height, subgrid_width = subgrids[0].shape
    separator_col = np.full((subgrid_height, 1), 6, dtype=int)
    output_parts = []

    # Reverse the order of subgrids
    reversed_subgrids = subgrids[::-1]

    for i, subgrid in enumerate(reversed_subgrids):
        output_parts.append(subgrid)
        if i < len(reversed_subgrids) - 1:
            output_parts.append(separator_col)

    return np.hstack(output_parts)


def assemble_quadrants(tl: np.ndarray, tr: np.ndarray, bl: np.ndarray, br: np.ndarray) -> np.ndarray:
    """Assembles quadrants vertically in specific order, separated by horizontal '6' rows."""
    subgrid_height, subgrid_width = tl.shape # Assume all quadrants have same shape
    separator_row = np.full((1, subgrid_width), 6, dtype=int)

    # Order: Top-Left, Bottom-Right, Top-Right, Bottom-Left
    ordered_quadrants = [tl, br, tr, bl]
    output_parts = []

    for i, quadrant in enumerate(ordered_quadrants):
        output_parts.append(quadrant)
        if i < len(ordered_quadrants) - 1:
            output_parts.append(separator_row)

    return np.vstack(output_parts)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying separators (rows/columns of 6s),
    extracting subgrids, and reassembling them based on the separator configuration.
    """
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # Find separators
    h_seps = find_horizontal_separators(grid)
    v_seps = find_vertical_separators(grid)

    # Determine configuration and extract/reassemble
    if h_seps and not v_seps:
        # Vertical Blocks configuration
        # Subgrids are extracted row-wise
        subgrids = extract_subgrids(grid, h_seps, [])
        # Reassemble horizontally, reversed order
        output_grid_np = assemble_vertical_blocks(subgrids)
    elif v_seps and not h_seps:
        # Horizontal Blocks configuration
        # Subgrids are extracted column-wise
        subgrids = extract_subgrids(grid, [], v_seps)
        # Reassemble vertically, original order
        output_grid_np = assemble_horizontal_blocks(subgrids)
    elif len(h_seps) == 1 and len(v_seps) == 1:
         # Potential Quadrants configuration
         # Extract assuming standard quadrant split - check if this matches all examples
         # Needs careful extraction based on the single horizontal and vertical separator
         h_sep = h_seps[0]
         v_sep = v_seps[0]

         tl = grid[0:h_sep, 0:v_sep]
         tr = grid[0:h_sep, v_sep+1:cols]
         bl = grid[h_sep+1:rows, 0:v_sep]
         br = grid[h_sep+1:rows, v_sep+1:cols]

         # Check if extraction yielded 4 quadrants (important for cases where separators are at edges)
         if tl.size > 0 and tr.size > 0 and bl.size > 0 and br.size > 0:
             output_grid_np = assemble_quadrants(tl, tr, bl, br)
         else: # Fallback or handle specific edge cases if needed - for now assume standard quadrants
              # This might happen if separators are at the very edge. Re-evaluate extraction if necessary.
              # Example: if grid is only 2 blocks separated by a vertical line.
              # Let's re-check extraction logic for this case based on general extraction
              subgrids = extract_subgrids(grid, h_seps, v_seps)
              # The default extraction handles this, but the order might be wrong for quadrants assembly.
              # Need a specific quadrant identification. Let's stick to the explicit split above for now.
              # If the simple split fails, maybe it should revert to horizontal/vertical block logic?
              # Based on examples, train_1 is quadrants, train_2 is vertical, train_3 is horizontal.
              # The simple split seems correct for train_1.
              # Let's assume if both h_seps and v_seps exist, it's the quadrant case as defined.
               output_grid_np = assemble_quadrants(tl, tr, bl, br) # Re-assert quadrant logic

    else:
        # Handle cases with no separators or complex separator patterns if needed
        # For now, assume one of the three patterns based on examples
        # If no separators, perhaps return the input grid?
        # Or if multiple separators in one direction? Example grids don't show this complexity.
        # Based on the examples provided, we only see single lines or single crossing lines.
        # If unexpected separators, return input? Or raise error? Let's return input for now.
         output_grid_np = grid # Default fallback

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    return output_grid
```
