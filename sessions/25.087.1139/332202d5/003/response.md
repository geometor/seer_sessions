```python
import numpy as np
import math
from typing import List, Tuple, Dict

"""
Transformation Rule:

1.  **Identify the Control Column:** Locate the vertical column (`azure_col`) characterized by containing both 'azure' (8) and 'blue' (1) pixels. This column acts as a control axis. The background color is often 'orange' (7) but can vary; assume it's the most frequent color overall or specifically avoid 1 and 8 when identifying marker colors.

2.  **Identify Marker Rows and Colors:** Scan the input grid row by row. A row `r` is a 'marker row' if the pixel at `input[r, azure_col]` is 'blue' (1). For each marker row, determine its associated 'marker color'. This is the predominant color in the row *other than* 'blue' (1) and the likely background color (e.g., 'orange' 7, or simply not 1 or 8). Store these findings, mapping marker row indices to their colors (e.g., `{marker_row_index: marker_color}`).

3.  **Determine Row Color Based on Proximity to Markers:**
    a.  Initialize an output grid of the same dimensions as the input.
    b.  Iterate through each row index `r` of the grid.
    c.  **If `r` is a marker row index:**
        i.  Fill the entire row `r` in the output grid with 'blue' (1).
        ii. Set the pixel at `output[r, azure_col]` to 'azure' (8).
    d.  **If `r` is *not* a marker row index:**
        i.  Calculate the vertical distance from row `r` to every marker row `m`: `distance = abs(r - m)`.
        ii. Find the minimum distance (`min_dist`) among these.
        iii. Identify all marker rows (`closest_markers`) that are at this `min_dist` from row `r`.
        iv. **Single Closest Marker:** If there is only one closest marker (`len(closest_markers) == 1`):
            - Get the `marker_color` associated with this single closest marker.
            - Fill the entire row `r` in the output grid with this `marker_color`.
            - Set the pixel at `output[r, azure_col]` to 'blue' (1).
        v.  **Multiple Closest Markers (Tie):** If there are multiple closest markers (`len(closest_markers) > 1`):
            - Check the `marker_color` associated with each of the tied closest markers.
            - **If all tied markers have the *same* `marker_color`:**
                - Fill the entire row `r` in the output grid with this common `marker_color`.
                - Set the pixel at `output[r, azure_col]` to 'blue' (1).
            - **If the tied markers have *different* `marker_colors`:**
                - Fill the entire row `r` in the output grid with 'blue' (1). (The pixel at `azure_col` will also be 'blue').

4.  **Return the Output Grid:** The fully processed grid is the result.
"""

import numpy as np
import math
from collections import Counter

def find_azure_col(grid: np.ndarray) -> int:
    """Finds the column index containing the vertical control line (azure 8 and blue 1)."""
    height, width = grid.shape
    for c in range(width):
        col_vals = grid[:, c]
        counts = np.bincount(col_vals, minlength=10)
        # A column is the control column if it contains both 8 and 1
        if counts[8] > 0 and counts[1] > 0:
            # Further check: ensure it's not just random 8s and 1s, but a dominant feature.
            # Often the rest is background (e.g., 7).
            # If the count of 8 + count of 1 is significant fraction of height, likely it.
             if counts[8] + counts[1] >= 1: # Simple check, might need refinement if noisy
                # Check if other numbers are mostly a single background color (like 7)
                other_colors = [val for val in col_vals if val != 8 and val != 1]
                if not other_colors or len(set(other_colors)) <= 1:
                     return c

    # Fallback if primary check fails (e.g., no background color in the column)
    for c in range(width):
        col_vals = grid[:, c]
        counts = np.bincount(col_vals, minlength=10)
        if counts[8] > 0 and counts[1] > 0:
            return c

    raise ValueError("Control column (containing 8s and 1s) not found.")

def find_marker_rows_and_colors(grid: np.ndarray, azure_col: int) -> Dict[int, int]:
    """Finds marker rows (blue '1' at azure_col) and their associated dominant color."""
    marker_info = {}
    height = grid.shape[0]
    # Determine potential background color (most frequent color overall?)
    # Simplified: Assume 7 is background if present, otherwise look for non-1/non-8.
    background_color = 7 # Default assumption based on examples
    if 7 not in grid:
         # If 7 isn't present, maybe the background is 0 or something else?
         # For now, just avoid 1 and 8.
         background_color = -1 # Indicate no specific background color to ignore

    for r in range(height):
        if grid[r, azure_col] == 1:
            marker_color = -1
            row_vals = grid[r, :]
            unique_colors = np.unique(row_vals)

            # Find the color that isn't blue (1) and isn't the azure_col marker (1)
            # and isn't the background color (7 or -1 if undetermined)
            possible_colors = [c for c in unique_colors if c != 1 and c != background_color and c != 8] # Also exclude 8 just in case

            if len(possible_colors) == 1:
                marker_color = possible_colors[0]
            elif len(possible_colors) > 1:
                 # If multiple possibilities, pick the most frequent one in the row (excluding 1 and background)
                 row_counts = Counter(row_vals)
                 best_color = -1
                 max_count = -1
                 for color in possible_colors:
                     if row_counts[color] > max_count:
                         max_count = row_counts[color]
                         best_color = color
                 marker_color = best_color
            # If no other color found (row is all 1s or 1s and background), this is unexpected.
            # Let's stick to requiring a distinct marker color.

            if marker_color != -1:
                marker_info[r] = marker_color
            else:
                 # If still -1, try finding any color != 1 in the row
                 fallback_colors = [c for c in unique_colors if c != 1]
                 if fallback_colors:
                     # Take the first one? Or most frequent? Let's try first.
                     marker_color = fallback_colors[0]
                     marker_info[r] = marker_color
                 # If row is ONLY 1s, this is an issue. Raise error? Or default?
                 # Based on examples, a marker color should always exist.
                 # else: raise ValueError(f"Marker row {r} has no identifiable marker color.")


    if not marker_info:
        raise ValueError("No marker rows (blue '1' in control column) found.")

    return marker_info


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on marker rows defined by a control column.
    Rows in the output grid are colored based on the color of the nearest marker row.
    Marker rows themselves become blue, intersecting the control column as azure.
    Rows equidistant between markers of different colors also become blue.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.zeros_like(input_np)

    # 1. Find the control column
    try:
        azure_col = find_azure_col(input_np)
    except ValueError as e:
        # Handle error: perhaps return input or a default grid?
        print(f"Error finding control column: {e}")
        # Return input unchanged if control column not found?
        return input_grid

    # 2. Find marker rows and their colors
    try:
        marker_info = find_marker_rows_and_colors(input_np, azure_col)
        marker_rows = sorted(marker_info.keys())
    except ValueError as e:
         # Handle error: No markers found
        print(f"Error finding markers: {e}")
        # What should happen if no markers? Fill with background? Return input?
        # Let's assume fill with a default (e.g., 0)
        return np.zeros_like(input_np).tolist()

    # 3. Fill rows based on proximity to markers
    for r in range(height):
        if r in marker_info:
            # 3.c. Marker row itself
            output_np[r, :] = 1  # Fill row with blue
            output_np[r, azure_col] = 8  # Set intersection to azure
        else:
            # 3.d. Non-marker row: Find closest marker(s)
            min_dist = float('inf')
            closest_markers = []
            for m_row in marker_rows:
                dist = abs(r - m_row)
                if dist < min_dist:
                    min_dist = dist
                    closest_markers = [m_row]
                elif dist == min_dist:
                    closest_markers.append(m_row)

            if len(closest_markers) == 1:
                # 3.d.iv. Single Closest Marker
                m_closest = closest_markers[0]
                fill_color = marker_info[m_closest]
                output_np[r, :] = fill_color
                output_np[r, azure_col] = 1 # Set control column pixel to blue
            else:
                # 3.d.v. Multiple Closest Markers (Tie)
                tied_colors = {marker_info[m] for m in closest_markers}
                if len(tied_colors) == 1:
                    # Tie with Same Colors
                    fill_color = list(tied_colors)[0]
                    output_np[r, :] = fill_color
                    output_np[r, azure_col] = 1 # Set control column pixel to blue
                else:
                    # Tie with Different Colors
                    output_np[r, :] = 1 # Fill row with blue

    return output_np.tolist()
```