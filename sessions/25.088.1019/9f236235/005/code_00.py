import numpy as np
import collections

"""
Divide an input grid based on separator lines, extract representative colors from the resulting cells, form a new grid from these colors, and flip the new grid horizontally.

1.  **Identify Separator Color:**
    *   Scan all rows and columns of the input grid.
    *   Identify potential separator colors: For each color C (not background color 0), find rows and columns that contain *only* C and the background color 0.
    *   Determine the `separator_color` as the color C that is associated with *both* potential horizontal separator rows *and* potential vertical separator columns. If multiple such colors exist, choose the one associated with the largest total number of potential rows and columns. If no single color is associated with both rows and columns, choose the color associated with the largest total number of potential rows or columns.
2.  **Identify Separator Indices:**
    *   Using the determined `separator_color`, scan the input grid again.
    *   Identify horizontal separator indices (`h_indices`): A row index `r` is included if all pixels in `input_grid[r, :]` are either `background_color` (0) or `separator_color`, AND at least one pixel in that row is `separator_color`.
    *   Identify vertical separator indices (`v_indices`): A column index `c` is included if all pixels in `input_grid[:, c]` are either `background_color` (0) or `separator_color`, AND at least one pixel in that column is `separator_color`.
3.  **Determine Logical Grid Structure:**
    *   Define horizontal boundaries using `h_indices` and the top/bottom edges of the input grid (index -1 and height).
    *   Define vertical boundaries using `v_indices` and the left/right edges of the input grid (index -1 and width).
    *   Calculate the logical grid dimensions (N rows, M columns) based on the number of regions between boundaries.
4.  **Create Intermediate Content Grid:**
    *   Initialize an intermediate grid (`content_grid`) of size N x M with the `background_color` (0).
5.  **Extract Content Colors:**
    *   Iterate through each logical cell (`r`, `c`) from `(0, 0)` to `(N-1, M-1)`.
    *   For each logical cell, identify the corresponding rectangular region of pixels in the input grid using the calculated boundaries.
    *   Examine the colors within this region. Find the set of unique colors excluding the `background_color` and the `separator_color`.
    *   If this set contains exactly one color, assign this color to `content_grid[r, c]`. Otherwise, leave it as the `background_color`.
6.  **Final Transformation:**
    *   Create the final `output_grid` by performing a horizontal flip (reflecting across the vertical axis) on the `content_grid`.
7.  **Return** the `output_grid`.
"""


def find_separator_color_and_strict_indices(grid):
    """
    Identifies the separator color and the strict indices of horizontal and vertical separator lines.
    A strict separator line contains ONLY the separator color and the background color,
    and must contain at least one instance of the separator color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (separator_color, h_indices, v_indices)
               - separator_color (int): The identified color of the separator lines.
               - h_indices (list): Sorted list of row indices containing horizontal separators.
               - v_indices (list): Sorted list of column indices containing vertical separators.

    Raises:
        ValueError: If a separator color cannot be determined.
    """
    height, width = grid.shape
    potential_colors = collections.defaultdict(lambda: {'rows': set(), 'cols': set()})
    background_color = 0

    # Step 1: Identify potential separator colors (initial broad check)
    # Check rows for potential colors
    for r in range(height):
        unique_colors = set(grid[r, :])
        non_bg_colors = unique_colors - {background_color}
        # A potential separator *row* for color identification might initially
        # just be predominantly one color, even if other stuff exists.
        # Let's use the original simpler logic to *find* candidate colors first.
        if len(non_bg_colors) == 1:
             color = non_bg_colors.pop()
             potential_colors[color]['rows'].add(r) # Store row index for potential color

    # Check columns for potential colors
    for c in range(width):
        unique_colors = set(grid[:, c])
        non_bg_colors = unique_colors - {background_color}
        if len(non_bg_colors) == 1:
             color = non_bg_colors.pop()
             potential_colors[color]['cols'].add(c) # Store col index for potential color


    # Determine the most likely separator color based on counts
    separator_color = -1
    max_lines = -1
    valid_candidates = [] # Colors that are candidates based on *any* row/col presence

    # Find candidates that appear in potential rows AND potential cols
    for color, indices in potential_colors.items():
        # Here we just check if the color *could* be a separator based on appearing
        # in at least one row-like structure and one col-like structure initially.
        if len(indices['rows']) > 0 and len(indices['cols']) > 0:
            valid_candidates.append(color)

    if not valid_candidates:
        # Fallback 1: No color found in both row and column structures.
        # Pick the color found in the most row/column structures overall.
        for color, indices in potential_colors.items():
            total_lines = len(indices['rows']) + len(indices['cols'])
            if total_lines > max_lines:
                max_lines = total_lines
                separator_color = color
    elif len(valid_candidates) == 1:
        # Exactly one color is a candidate for both row and column separators.
        separator_color = valid_candidates[0]
    else:
        # Multiple candidates found in both row and col structures.
        # Pick the candidate forming the most lines total among these valid candidates.
        for color in valid_candidates:
            total_lines = len(potential_colors[color]['rows']) + len(potential_colors[color]['cols'])
            if total_lines > max_lines:
                max_lines = total_lines
                separator_color = color

    if separator_color == -1:
         # Fallback 2: Still no candidate found (e.g., grid only has background).
         # Check if any potential colors were found at all
         if not potential_colors:
             raise ValueError("Could not determine separator color. No potential separator lines found.")
         else:
             # Re-run fallback 1 logic just in case something was missed.
             for color, indices in potential_colors.items():
                 total_lines = len(indices['rows']) + len(indices['cols'])
                 if total_lines > max_lines:
                     max_lines = total_lines
                     separator_color = color
             if separator_color == -1: # Final check
                 raise ValueError("Could not determine separator color after fallback checks.")


    # Step 2: Identify STRICT separator indices using the determined separator_color
    h_indices = []
    v_indices = []

    # Check rows for strict horizontal separators
    for r in range(height):
        row_colors = set(grid[r, :])
        # Strict condition: only background and separator color allowed
        if row_colors <= {background_color, separator_color}:
            # Strict condition: must contain at least one separator color pixel
            if separator_color in row_colors:
                h_indices.append(r)

    # Check columns for strict vertical separators
    for c in range(width):
        col_colors = set(grid[:, c])
        # Strict condition: only background and separator color allowed
        if col_colors <= {background_color, separator_color}:
             # Strict condition: must contain at least one separator color pixel
            if separator_color in col_colors:
                v_indices.append(c)

    return separator_color, sorted(h_indices), sorted(v_indices)


def transform(input_grid):
    """
    Transforms the input grid based on the identified logical grid structure and content.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # 1 & 2: Identify separator color and strict line indices using the helper function
    try:
        separator_color, h_sep_indices, v_sep_indices = find_separator_color_and_strict_indices(input_np)
    except ValueError as e:
        # Handle cases where no separator is found, potentially return input or default
        # For now, return a 1x1 background grid if separation fails.
        print(f"Warning: Could not find separator - {e}. Returning default grid.")
        # Let's try extracting content from the whole grid if separation fails
        unique_colors = set(input_np.flatten()) - {background_color} # Check without assuming separator
        if len(unique_colors) == 1:
             content_color = unique_colors.pop()
             return [[content_color]] # Return 1x1 grid with the single found color
        else:
             return [[background_color]] # Return 1x1 background if multiple colors or only bg


    # 3. Determine logical grid boundaries
    # Add -1 and grid dimension to capture edges relative to separators
    h_boundaries = sorted(list(set([-1] + h_sep_indices + [height])))
    v_boundaries = sorted(list(set([-1] + v_sep_indices + [width])))

    # Calculate logical grid dimensions
    num_rows_logical = len(h_boundaries) - 1
    num_cols_logical = len(v_boundaries) - 1

    # Handle edge case: if no strict separators found, dimensions might be 1x1
    if num_rows_logical <= 0 or num_cols_logical <= 0:
         # This implies the grid might be composed entirely of separator/background
         # or the logic above needs refinement.
         # Let's analyze the whole grid as one cell in this case.
         unique_colors_in_region = set(input_np.flatten()) - {background_color, separator_color}
         if len(unique_colors_in_region) == 1:
             content_color = unique_colors_in_region.pop()
             # Flip a 1x1 grid (no change)
             return [[content_color]]
         else:
             # If no single content color or no separators, return background
             return [[background_color]]


    # 4. Create intermediate content grid, initialized with background color
    content_grid = np.full((num_rows_logical, num_cols_logical), background_color, dtype=int)

    # 5. Iterate through logical grid cells and extract content colors
    for r in range(num_rows_logical):
        # Define row boundaries for the current logical cell's region in input grid
        # Start index is 1 after the previous boundary/separator
        row_start = h_boundaries[r] + 1
        # End index is the index of the next boundary/separator (exclusive)
        row_end = h_boundaries[r+1]

        for c in range(num_cols_logical):
            # Define column boundaries for the current logical cell's region
            col_start = v_boundaries[c] + 1
            col_end = v_boundaries[c+1]

            # Ensure region is valid (start < end)
            if row_start >= row_end or col_start >= col_end:
                # This can happen if separators are adjacent. Leave as background.
                continue

            # Extract the region from the input grid
            region = input_np[row_start:row_end, col_start:col_end]

            # Find unique non-background, non-separator color(s) in the region
            unique_colors_in_region = set(region.flatten()) - {background_color, separator_color}

            # Assign color to content_grid if exactly one unique content color exists
            if len(unique_colors_in_region) == 1:
                content_color = unique_colors_in_region.pop()
                content_grid[r, c] = content_color
            # Otherwise, it remains background_color (0) as initialized

    # 6. Perform horizontal flip on the intermediate grid
    output_grid_np = np.fliplr(content_grid)

    # 7. Return the result as list of lists
    return output_grid_np.tolist()