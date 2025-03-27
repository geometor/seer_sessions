```python
import numpy as np

"""
Transforms a pattern found inside a blue rectangular frame using colors from the 
input grid's corners as replacement colors based on quadrants.

1.  Identify Corner Colors: Record the colors of the four pixels at the 
    absolute corners (top-left, top-right, bottom-left, bottom-right) of the 
    input grid (TL_color, TR_color, BL_color, BR_color).
2.  Locate Central Azure Pattern: Find the bounding box of all Azure (8) pixels 
    in the input grid.
3.  Identify Inner Frame Boundaries: Assume the relevant Blue (1) frame is 
    exactly one pixel outside the bounding box of the Azure pixels. Calculate 
    the frame's min/max row/column indices.
4.  Extract Inner Pattern: Extract the subgrid located strictly *inside* the 
    inner frame boundaries. Let its dimensions be H_inner x W_inner.
5.  Initialize Output Grid: Create a new grid of size H_inner x W_inner, 
    filled with White (0).
6.  Map Colors: Iterate through each pixel (r, c) in the extracted inner pattern.
    - If the inner pattern pixel is White (0), the output pixel remains White (0).
    - If the inner pattern pixel is Azure (8):
        - Determine its quadrant within the inner pattern relative to the center 
          (H_inner // 2, W_inner // 2).
        - Assign the corresponding corner color (TL_color, TR_color, BL_color, 
          BR_color) to the output pixel.
    - Other colors in the inner pattern map to White (0).
7.  Return the resulting output grid.
"""

def _find_azure_bbox(grid: np.ndarray) -> tuple[int, int, int, int] | None:
    """
    Finds the bounding box of Azure (8) pixels in the grid.

    Args:
        grid: The input numpy array grid.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) representing the 
        bounding box (inclusive). Returns None if no Azure pixels are found.
    """
    azure_coords = np.argwhere(grid == 8)
    if azure_coords.size == 0:
        return None
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])
    return min_row, max_row, min_col, max_col

def _get_corner_colors(grid: np.ndarray) -> tuple[int, int, int, int]:
    """
    Extracts the colors of the four corner pixels.

    Args:
        grid: The input numpy array grid.

    Returns:
        A tuple (TL_color, TR_color, BL_color, BR_color).
    """
    H, W = grid.shape
    TL_color = grid[0, 0]
    TR_color = grid[0, W - 1]
    BL_color = grid[H - 1, 0]
    BR_color = grid[H - 1, W - 1]
    return TL_color, TR_color, BL_color, BR_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the quadrant-based color replacement transformation.

    Args:
        input_grid: The input grid represented as a 2D list.

    Returns:
        The transformed output grid as a 2D list. Returns empty list
        if the expected structure (Azure pattern, frame) is not found.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Handle grids too small to contain corners, frame, and pattern
    if H < 3 or W < 3:
        # print("Warning: Input grid too small.")
        return [] 

    # --- Step 1: Identify Corner Colors ---
    TL_color, TR_color, BL_color, BR_color = _get_corner_colors(input_np)

    # --- Step 2: Locate Central Azure Pattern ---
    azure_bbox = _find_azure_bbox(input_np)
    if azure_bbox is None:
        # print("Warning: No Azure (8) pixels found.")
        # Fallback or error handling could be added here if needed.
        # Based on examples, Azure pattern is expected.
        return [] # Return empty list if core pattern element is missing

    azure_min_r, azure_max_r, azure_min_c, azure_max_c = azure_bbox

    # --- Step 3: Identify Inner Frame Boundaries ---
    # Assume the frame is exactly one pixel outside the Azure bbox
    frame_min_r = azure_min_r - 1
    frame_max_r = azure_max_r + 1
    frame_min_c = azure_min_c - 1
    frame_max_c = azure_max_c + 1

    # Basic validation: Check if frame boundaries are within grid limits
    if not (0 <= frame_min_r < frame_max_r < H and 0 <= frame_min_c < frame_max_c < W):
         # print("Warning: Deduced frame boundaries extend outside grid or are invalid.")
         # This might indicate an unexpected input structure.
         return []

    # Optional: Verify frame pixels are actually Blue (1) - might be needed for robustness
    # Example check (can be expanded):
    # if not np.all(input_np[frame_min_r, frame_min_c+1:frame_max_c] == 1): return [] # Check top edge
    # ... check other edges ...

    # --- Step 4: Extract Inner Pattern ---
    # The inner pattern is strictly inside the frame boundaries
    inner_min_r = frame_min_r + 1
    inner_max_r = frame_max_r # Slice index is exclusive
    inner_min_c = frame_min_c + 1
    inner_max_c = frame_max_c # Slice index is exclusive

    inner_pattern = input_np[inner_min_r:inner_max_r, inner_min_c:inner_max_c]
    H_inner, W_inner = inner_pattern.shape

    # Check if inner pattern is valid
    if H_inner <= 0 or W_inner <= 0:
        # print("Warning: Invalid frame or no inner pattern extracted.")
        return [] 

    # --- Step 5: Initialize Output Grid ---
    # Initialize with White (0), as White pixels map directly
    output_grid = np.zeros_like(inner_pattern)

    # --- Step 6: Map Colors ---
    # Calculate the midpoints for quadrant division (integer division)
    # Note: If H_inner or W_inner is odd, the middle row/col falls into 
    # the bottom/right quadrant respectively due to zero-based indexing 
    # and '<' vs '>=' comparisons. This matches the examples' implied logic.
    mid_row = H_inner // 2
    mid_col = W_inner // 2

    # Iterate through each pixel of the inner pattern
    for r in range(H_inner):
        for c in range(W_inner):
            current_color = inner_pattern[r, c]

            if current_color == 8: # Azure pixel
                # Determine the quadrant based on row and column relative to midpoints
                if r < mid_row and c < mid_col: # Top-Left Quadrant
                    output_grid[r, c] = TL_color
                elif r < mid_row and c >= mid_col: # Top-Right Quadrant
                    output_grid[r, c] = TR_color
                elif r >= mid_row and c < mid_col: # Bottom-Left Quadrant
                    output_grid[r, c] = BL_color
                elif r >= mid_row and c >= mid_col: # Bottom-Right Quadrant
                    output_grid[r, c] = BR_color
            # White (0) pixels are already handled by initialization
            # Other colors in inner_pattern also remain 0 in output_grid

    # --- Step 7: Return Output Grid ---
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```