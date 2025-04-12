```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the arrangement of '6' separators and pattern regions (digits other than 6 or 7).

The transformation operates in one of three modes determined by the separators:

1.  **Split Vertical Mode:** Activated if *only* vertical separators ('6' columns) exist and they perfectly partition the grid columns into segments suitable for the number of patterns found (assuming a standard 5-column width per pattern). Subgrids are extracted left-to-right and stacked vertically in the output, separated by horizontal lines of '6's.

2.  **Split Horizontal Mode:** Activated if *only* horizontal separators ('6' rows) exist, there's more than one, and they perfectly partition the grid rows into segments suitable for the number of patterns (assuming a standard 5-row height per pattern). Subgrids are extracted, ordered from bottom-to-top, and concatenated horizontally in the output, separated by vertical lines of '6's.

3.  **Extract Region Mode:** Activated in other cases (e.g., mixed separators, a single horizontal separator, no perfect partitioning). Connected pattern regions are identified. For each region, its bounding box content is copied into the top-left of a 5x5 panel (padded with '7's). Panels are ordered based on the original region's position relative to the primary horizontal separator (if any) and grid center: Top-Left, Bottom-Right, Top-Right, Bottom-Left. The ordered panels are stacked vertically in the output, separated by horizontal lines of '6's.
"""

def find_horizontal_separators(grid_np):
    """Finds indices of rows composed entirely of 6."""
    separator_digit = 6
    rows, _ = grid_np.shape
    separator_indices = []
    for r in range(rows):
        if np.all(grid_np[r, :] == separator_digit):
            separator_indices.append(r)
    return separator_indices

def find_vertical_separators(grid_np):
    """Finds indices of columns composed entirely of 6."""
    separator_digit = 6
    _, cols = grid_np.shape
    separator_indices = []
    for c in range(cols):
        if np.all(grid_np[:, c] == separator_digit):
            separator_indices.append(c)
    return separator_indices

def count_patterns(grid_np):
    """Counts distinct connected regions of non-background (7) and non-separator (6) digits."""
    background_digit = 7
    separator_digit = 6
    mask = (grid_np != background_digit) & (grid_np != separator_digit)
    _, num_features = label(mask)
    return num_features

def check_partitioning(grid_shape, separator_indices, num_patterns, axis):
    """
    Checks if separators perfectly partition the grid along the given axis,
    assuming a standard pattern size of 5x5.
    """
    rows, cols = grid_shape
    pattern_dim_size = 5 # Assumed standard dimension (height or width) for patterns
    num_separators = len(separator_indices)

    if axis == 0: # Horizontal separators, check rows
        expected_rows = num_patterns * pattern_dim_size + num_separators
        return rows == expected_rows
    else: # Vertical separators, check columns
        expected_cols = num_patterns * pattern_dim_size + num_separators
        return cols == expected_cols

def get_subgrids(grid_np, separator_indices, axis):
    """Extracts subgrids based on separator indices along a given axis."""
    subgrids = []
    start = 0
    for idx in separator_indices:
        if axis == 0: # Horizontal separators -> split rows
            subgrid = grid_np[start:idx, :]
        else: # Vertical separators -> split columns
            subgrid = grid_np[:, start:idx]
        # Only add if the subgrid is not empty (can happen with adjacent separators)
        if subgrid.size > 0:
            subgrids.append(subgrid)
        start = idx + 1
    # Add the last subgrid after the last separator
    if axis == 0:
        subgrid = grid_np[start:, :]
    else:
        subgrid = grid_np[:, start:]
    if subgrid.size > 0:
        subgrids.append(subgrid)
    return subgrids

def create_panel(region_slice_data):
    """Creates a 5x5 panel and places the region slice data in the top-left."""
    panel_size = 5
    background_digit = 7
    panel = np.full((panel_size, panel_size), background_digit, dtype=int)
    h, w = region_slice_data.shape
    # Ensure the slice fits within the panel size
    copy_h = min(h, panel_size)
    copy_w = min(w, panel_size)
    panel[0:copy_h, 0:copy_w] = region_slice_data[0:copy_h, 0:copy_w]
    return panel


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    background_digit = 7
    separator_digit = 6

    # --- 1. Analyze Grid Structure ---
    h_separators = find_horizontal_separators(grid_np)
    v_separators = find_vertical_separators(grid_np)
    num_patterns = count_patterns(grid_np)

    # --- 2. Determine Transformation Mode ---
    mode = 'extract_region' # Default mode
    partitions_v = False
    partitions_h = False

    if num_patterns > 0: # Partitioning only makes sense if there are patterns
        if v_separators and not h_separators:
             partitions_v = check_partitioning(grid_np.shape, v_separators, num_patterns, axis=1)
             if partitions_v:
                 mode = 'split_vertical'
        elif h_separators and not v_separators and len(h_separators) > 0: # Check horizontal only if vertical didn't match
             # Mode 2 requires more than one separator for unambiguous partitioning in examples
             partitions_h = check_partitioning(grid_np.shape, h_separators, num_patterns, axis=0)
             if partitions_h and len(h_separators) >= 1 : # Relaxed condition slightly from >1 to >=1
                 mode = 'split_horizontal'


    # --- 3. Execute Transformation ---
    output_grid_np = None

    # ** Mode 1: Split Vertical **
    if mode == 'split_vertical':
        subgrids = get_subgrids(grid_np, v_separators, axis=1)
        # Keep original left-to-right order
        if subgrids:
            output_parts = []
            # Define horizontal separator shape based on subgrid width
            separator_row = np.full((1, subgrids[0].shape[1]), separator_digit, dtype=int)
            for i, subgrid in enumerate(subgrids):
                output_parts.append(subgrid)
                if i < len(subgrids) - 1:
                    output_parts.append(separator_row)
            if output_parts:
                output_grid_np = np.vstack(output_parts)

    # ** Mode 2: Split Horizontal **
    elif mode == 'split_horizontal':
        subgrids = get_subgrids(grid_np, h_separators, axis=0)
        # Reverse order (bottom-to-top)
        subgrids.reverse()
        if subgrids:
            output_parts = []
             # Define vertical separator shape based on subgrid height
            separator_col = np.full((subgrids[0].shape[0], 1), separator_digit, dtype=int)
            for i, subgrid in enumerate(subgrids):
                output_parts.append(subgrid)
                if i < len(subgrids) - 1:
                    output_parts.append(separator_col)
            if output_parts:
                output_grid_np = np.hstack(output_parts)

    # ** Mode 3: Extract Region **
    elif mode == 'extract_region':
        mask = (grid_np != background_digit) & (grid_np != separator_digit)
        labeled_array, _ = label(mask)
        objects_slices = find_objects(labeled_array)

        if not objects_slices: # Handle case with no patterns found
             return []

        regions = []
        primary_separator_idx = h_separators[0] if h_separators else -1 # Use first H sep if exists

        for i, slc in enumerate(objects_slices):
            # Extract the bounding box content
            region_data = grid_np[slc]
            # Create the 5x5 panel
            panel = create_panel(region_data)

            # Determine position relative to the separator and center
            # Use the top-left corner of the bounding box for position determination
            top_row = slc[0].start
            left_col = slc[1].start

            # Simplified position logic based on examples
            is_above = top_row < primary_separator_idx if primary_separator_idx != -1 else top_row < rows / 2
            is_left = left_col < cols / 2

            pos_key = ""
            if is_above:
                pos_key += "T"
            else:
                pos_key += "B"
            if is_left:
                pos_key += "L"
            else:
                pos_key += "R"

            regions.append({'panel': panel, 'pos': pos_key, 'slice': slc})

        # Sort regions based on the observed order: TL, BR, TR, BL
        sort_order = {'TL': 0, 'BR': 1, 'TR': 2, 'BL': 3}
        # Add fallback sort by position if keys missing or duplicate
        regions.sort(key=lambda r: (sort_order.get(r['pos'], 99), r['slice'][0].start, r['slice'][1].start) )

        # Assemble panels vertically with horizontal separators
        output_parts = []
        panel_width = 5 # Assuming 5x5 panels
        separator_row = np.full((1, panel_width), separator_digit, dtype=int)
        for i, region in enumerate(regions):
            output_parts.append(region['panel'])
            # Add separator if not the last panel
            if i < len(regions) - 1:
                output_parts.append(separator_row)

        if output_parts: # Check if any regions were processed
             output_grid_np = np.vstack(output_parts)


    # --- 4. Final Output ---
    # Convert final numpy array back to list of lists
    if output_grid_np is None or output_grid_np.size == 0:
        # If no mode applied successfully or no patterns/subgrids were generated
        return []
    else:
        return output_grid_np.tolist()
```