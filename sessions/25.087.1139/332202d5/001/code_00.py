import numpy as np
from typing import List, Tuple

"""
Identify the vertical 'azure' (8) line and its column index (azure_col).
Identify 'marker rows' where the pixel at azure_col is 'blue' (1).
For each marker row, determine its associated 'marker color' (the color in the row other than 'blue' (1) and 'orange' (7)).
Create an output grid.
Iterate through each row 'r' of the output grid:
  Find the marker row immediately above or including row 'r'. If 'r' is above the first marker row, use the first marker row's color.
  Fill row 'r' with the marker color found.
After filling all rows based on the marker colors above them:
  Iterate through the marker rows again:
    Overwrite the marker row in the output grid with 'blue' (1).
Finally, adjust the azure_col in the output grid:
  Set all pixels in azure_col to 'blue' (1).
  Set the pixels in azure_col corresponding to the marker rows to 'azure' (8).
"""

def find_azure_col(grid: np.ndarray) -> int:
    """Finds the column index containing the vertical azure (8) line."""
    height, width = grid.shape
    for c in range(width):
        if np.all(grid[:, c] != 7): # Check if column has non-orange values, likely the azure line context
             # More robust check: find column with 8s and 1s primarily
             counts = np.bincount(grid[:, c], minlength=10)
             if counts[8] > 0 and counts[1] > 0:
                 return c
    # Fallback: Find first column containing an 8
    for c in range(width):
        if 8 in grid[:, c]:
            return c
    raise ValueError("Azure column (8) not found in the input grid.")

def find_marker_rows_and_colors(grid: np.ndarray, azure_col: int) -> List[Tuple[int, int]]:
    """Finds marker rows (blue '1' at azure_col) and their associated dominant color."""
    marker_info = []
    height = grid.shape[0]
    for r in range(height):
        if grid[r, azure_col] == 1:
            marker_color = -1  # Default/error value
            for c_val in grid[r, :]:
                # Find the color that isn't the marker (1) or background (7)
                if c_val != 1 and c_val != 7:
                    marker_color = c_val
                    break
            if marker_color != -1:
                 marker_info.append((r, marker_color))
            else:
                # Handle edge case if row only contains 1 and 7 (shouldn't happen based on examples)
                # Let's try finding any color not 7 in the row as a fallback
                 for c_val in grid[r, :]:
                     if c_val != 7:
                        marker_color = c_val
                        break
                 if marker_color != -1:
                     marker_info.append((r, marker_color))
                 else: # If truly only 7s, maybe use 0? This seems unlikely for ARC.
                     marker_info.append((r, 0)) # Defaulting to 0 if no other color found

    if not marker_info:
        raise ValueError("No marker rows (blue '1' in azure column) found.")

    # Sort by row index just in case they weren't found in order
    marker_info.sort(key=lambda item: item[0])
    return marker_info

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on marker rows and colors.

    Identifies a vertical 'azure' line and horizontal 'marker rows' indicated by
    a 'blue' pixel on the azure line. The color of the marker row determines the
    fill color for the region below it, until the next marker row. Marker rows
    themselves become 'blue', with the intersection point becoming 'azure'.
    The vertical line remains 'blue' except at these intersections.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.zeros_like(input_np)

    # Find the column with the azure line
    azure_col = find_azure_col(input_np)

    # Find marker rows and their associated colors
    marker_info = find_marker_rows_and_colors(input_np, azure_col)
    marker_row_indices = {info[0] for info in marker_info}

    # Fill the output grid based on marker regions
    current_marker_index = 0
    for r in range(height):
        # Find the marker that defines the color for this row
        # If r is above the first marker, use the first marker's color
        # Otherwise, use the color of the last marker whose index is <= r
        relevant_marker_idx = 0
        for i in range(len(marker_info)):
            if marker_info[i][0] <= r:
                relevant_marker_idx = i
            else:
                break # Markers are sorted, no need to check further

        fill_color = marker_info[relevant_marker_idx][1]
        output_np[r, :] = fill_color

    # Overwrite marker rows with blue (1)
    for r_idx, _ in marker_info:
        output_np[r_idx, :] = 1

    # Set the azure column correctly
    output_np[:, azure_col] = 1  # Default to blue
    for r_idx, _ in marker_info:
        output_np[r_idx, azure_col] = 8 # Set intersections to azure

    return output_np.tolist()