"""
Identifies horizontal (H) and/or vertical (V) separators (rows/columns of magenta color 6) in the input grid.
Extracts the panels (subgrids) defined by these separators.
Determines the output arrangement and panel ordering based on separator presence:
- If V separators exist (V-only or Both H and V): Arrange panels vertically.
    - If ONLY V separators exist (V-only): Order panels top-to-bottom, then left-to-right (base order).
    - If BOTH H and V separators exist (Both): Assuming a 2x2 panel grid, order panels as [Top-Left, Bottom-Right, Top-Right, Bottom-Left] based on their original positions.
- Else if ONLY H separators exist (H-only): Arrange panels horizontally. Order panels top-to-bottom, then left-to-right, and then REVERSE this order.
- Else (no separators): Return the input grid unchanged.
Constructs the output grid by assembling the ordered panels along the determined axis, inserting single magenta separators (rows for vertical, columns for horizontal) between them.
"""

import numpy as np
from typing import List, Tuple

def find_horizontal_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of rows consisting entirely of magenta (6)."""
    h_indices = []
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 6):
            h_indices.append(r)
    return h_indices

def find_vertical_separators(grid: np.ndarray) -> List[int]:
    """Finds indices of columns consisting entirely of magenta (6)."""
    v_indices = []
    for c in range(grid.shape[1]):
        if np.all(grid[:, c] == 6):
            v_indices.append(c)
    return v_indices

def extract_panels(grid: np.ndarray, h_seps: List[int], v_seps: List[int]) -> List[Tuple[np.ndarray, Tuple[int, int]]]:
    """Extracts panels based on separator indices, returning panels and their top-left coords."""
    panels = []
    rows, cols = grid.shape

    # Define the start and end rows for slicing panels
    row_starts = [0] + [h + 1 for h in h_seps]
    row_ends = h_seps + [rows]

    # Define the start and end columns for slicing panels
    col_starts = [0] + [v + 1 for v in v_seps]
    col_ends = v_seps + [cols]

    # Iterate through the potential panel locations
    for i in range(len(row_starts)):
        r_start, r_end = row_starts[i], row_ends[i]
        if r_start >= r_end: # Skip if start is not before end (e.g., adjacent separators)
            continue
        for j in range(len(col_starts)):
            c_start, c_end = col_starts[j], col_ends[j]
            if c_start >= c_end: # Skip if start is not before end
                continue

            # Extract the panel
            panel = grid[r_start:r_end, c_start:c_end]

            # Add the panel and its original top-left coordinates if it's not empty
            if panel.size > 0:
                panels.append((panel, (r_start, c_start)))

    return panels

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by identifying separators, extracting panels,
    and rearranging them vertically or horizontally based on the separator type and specific ordering rules.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # Step 1: Analyze Separators - Find horizontal and vertical magenta lines
    h_sep_indices = find_horizontal_separators(grid)
    v_sep_indices = find_vertical_separators(grid)

    has_h_seps = len(h_sep_indices) > 0
    has_v_seps = len(v_sep_indices) > 0

    # Step 3: Determine Scenario and Arrangement
    # Scenario 1: No Separators
    if not has_h_seps and not has_v_seps:
        return input_grid # Return input unchanged

    # Step 2: Extract Panels
    extracted_panels_with_coords = extract_panels(grid, h_sep_indices, v_sep_indices)

    # Handle edge case where extraction might yield no panels (e.g., grid is all separators)
    if not extracted_panels_with_coords:
        # This might happen if the grid consists only of separators or empty regions.
        # Returning an empty grid or the input might be options, choosing empty for now.
        return [[]]

    # Continue Step 3: Determine Arrangement Axis based on separator types
    # Vertical arrangement if V separators exist (covers V-Only and Both scenarios)
    arrange_vertically = has_v_seps
    # Horizontal arrangement only if H separators exist AND V separators DO NOT exist (H-Only scenario)
    arrange_horizontally = has_h_seps and not has_v_seps

    # Step 4: Order Panels
    # Calculate base order: Sort panels by original position (top-to-bottom, then left-to-right)
    sorted_panels_with_coords = sorted(extracted_panels_with_coords, key=lambda item: item[1])
    base_ordered_panels = [p[0] for p in sorted_panels_with_coords]

    final_ordered_panels = []

    if arrange_vertically:
        if has_h_seps: # Scenario 4: Both H and V separators exist
             # Specific permutation for 2x2 case seen in Example 1: [TL, BR, TR, BL] -> indices [0, 3, 1, 2]
             if len(base_ordered_panels) == 4: # Apply only if it's a 2x2 panel layout
                 final_ordered_panels = [
                     base_ordered_panels[0], # Top-Left
                     base_ordered_panels[3], # Bottom-Right
                     base_ordered_panels[1], # Top-Right
                     base_ordered_panels[2]  # Bottom-Left
                 ]
             else:
                 # Fallback or error handling for 'Both' cases not matching 2x2 panel structure
                 # For now, use base order as a guess, though this might be incorrect for other 'Both' layouts
                 print(f"Warning: 'Both' separator case encountered with {len(base_ordered_panels)} panels, not 4. Using base order.")
                 final_ordered_panels = base_ordered_panels
        else: # Scenario 3: Only V separators exist
            # Use the base order directly
            final_ordered_panels = base_ordered_panels

    elif arrange_horizontally: # Scenario 2: Only H separators exist
        # Reverse the base order
        final_ordered_panels = list(reversed(base_ordered_panels))
    else:
        # This path should logically not be reached due to the initial 'no separators' check
        return input_grid # Fallback

    # Check if panels list is empty after ordering logic (unlikely but possible)
    if not final_ordered_panels:
         return [[]]

    # Step 5: Assemble Output Grid
    output_grid_np = None
    num_panels = len(final_ordered_panels)

    if arrange_vertically:
        # Check panel width consistency for vertical stacking
        panel_width = final_ordered_panels[0].shape[1]
        if not all(p.shape[1] == panel_width for p in final_ordered_panels):
             print("Error: Panels have inconsistent widths for vertical stacking.")
             return [[]] # Return empty grid on error

        # Create a horizontal separator row (magenta)
        h_separator = np.full((1, panel_width), 6, dtype=int)

        # Stack panels vertically, inserting separators
        output_grid_np = final_ordered_panels[0]
        for i in range(1, num_panels):
            output_grid_np = np.vstack((output_grid_np, h_separator, final_ordered_panels[i]))

    elif arrange_horizontally:
        # Check panel height consistency for horizontal concatenation
        panel_height = final_ordered_panels[0].shape[0]
        if not all(p.shape[0] == panel_height for p in final_ordered_panels):
            print("Error: Panels have inconsistent heights for horizontal stacking.")
            return [[]] # Return empty grid on error

        # Create a vertical separator column (magenta)
        v_separator = np.full((panel_height, 1), 6, dtype=int)

        # Concatenate panels horizontally, inserting separators
        output_grid_np = final_ordered_panels[0]
        for i in range(1, num_panels):
            output_grid_np = np.hstack((output_grid_np, v_separator, final_ordered_panels[i]))

    # If no arrangement happened (should be covered by earlier checks)
    if output_grid_np is None:
        return input_grid # Fallback, though unlikely

    # Step 6: Return Output
    # Convert the final NumPy array back to a list of lists
    return output_grid_np.tolist()