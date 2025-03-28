import numpy as np

"""
The transformation determines the output grid by applying the first matching rule from the following prioritized list, using red (2) as the primary color and white (0) as the background color:

1.  **Solid Row Separation Rule:** Check if the input grid contains exactly three unique colors AND if it has a horizontal row composed entirely of the primary color (red). If both conditions are true:
    *   Identify the 'third color' (neither white nor red).
    *   Find the row index (`sr`) of the topmost solid red row.
    *   Create the output grid by filling rows `0` to `sr-1` with white, row `sr` with red, and rows `sr+1` to the bottom with the 'third color'.

2.  **Fixed Diagonal Pattern Rule:** If Rule 1 does not apply, check if the input grid contains exactly three unique colors AND if *all* red pixels are located at positions `(r, c)` where `r = c + 1` or `r = c + 2`. If both conditions are true:
    *   Identify the 'third color'.
    *   Create the output grid with a fixed pattern: pixels where `r < c + 1` are white, pixels where `r == c + 1` or `r == c + 2` are red, and pixels where `r > c + 2` are the 'third color'.

3.  **Column Filter with Conditional Downward Propagation Rule:** If neither Rule 1 nor Rule 2 applies, construct the output grid by processing each column independently based on the input grid:
    *   Find the row index (`mr`) of the topmost red pixel in the input column.
    *   If no red pixel exists in the input column, the output column is identical to the input column.
    *   If a topmost red pixel exists at `mr` in the input column:
        *   Initialize the corresponding output column.
        *   Set rows `0` to `mr-1` in the output column to white.
        *   Set the pixel at `(mr, col)` in the output column to red.
        *   For each row `r` from `mr + 1` downwards to the bottom of the grid:
            *   Examine the pixel at `(r, col)` in the *input* grid.
            *   If the input pixel `input_grid[r, col]` is white (0), set the output pixel `output_grid[r, col]` to the color of the pixel directly above it in the *output* grid (`output_grid[r - 1, col]`).
            *   Otherwise (if `input_grid[r, col]` is not white), set the output pixel `output_grid[r, col]` to its original color from the input grid (`input_grid[r, col]`).
"""

# --- Helper Functions ---

def find_unique_colors(grid):
    """Identifies unique colors in the grid."""
    return set(grid.flatten())

def find_solid_row(grid, color):
    """Finds the index of the first row consisting entirely of the specified color. Returns -1 if none found."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == color):
            return r
    return -1

def check_all_key_on_diag(grid, key_color):
    """Checks if all occurrences of key_color are on diagonals r=c+1 or r=c+2."""
    key_locations = np.argwhere(grid == key_color)
    if len(key_locations) == 0:
        # Rule 2 requires 3 colors, one of which must be the key color.
        # If no key color exists, Rule 2 cannot apply.
        return False
    for r, c in key_locations:
        if not (r == c + 1 or r == c + 2):
            return False
    return True

# --- Rule Application Functions ---

def apply_row_separation(grid_shape, key_color, background_color, third_color, solid_row_index):
    """Applies Rule 1: Row Separation."""
    height, width = grid_shape
    output_grid = np.full(grid_shape, background_color, dtype=int) # Fill above with background initially

    # Set the separator row
    output_grid[solid_row_index, :] = key_color

    # Fill below with third color, only if there are rows below
    if solid_row_index < height - 1:
        output_grid[solid_row_index + 1:, :] = third_color

    return output_grid

def apply_fixed_pattern(grid_shape, key_color, background_color, third_color):
    """Applies Rule 2: Fixed Diagonal Pattern Generation."""
    height, width = grid_shape
    output_grid = np.full(grid_shape, background_color, dtype=int) # Default to background

    for r in range(height):
        for c in range(width):
            # Key color diagonal band
            if r == c + 1 or r == c + 2:
                output_grid[r, c] = key_color
            # Third color below the band
            elif r > c + 2:
                output_grid[r, c] = third_color
            # Background color above the band (already set by default)

    return output_grid

def apply_column_filter_propagation(input_grid, key_color, background_color):
    """Applies Rule 3: Column Filtering with Conditional Downward Propagation."""
    height, width = input_grid.shape
    output_grid = np.copy(input_grid) # Start with a copy of the input

    for c in range(width):
        # Find the row index of the highest occurrence (minimum row index) of the key color in the input column
        key_color_indices = np.where(input_grid[:, c] == key_color)[0]

        if len(key_color_indices) > 0:
            min_row = np.min(key_color_indices)

            # 1. Set pixels above the highest key color to background in the output
            output_grid[:min_row, c] = background_color

            # 2. Set the topmost key color pixel itself to the key color in the output
            #    (This overwrites whatever might have been there in the input, ensuring it's the key color)
            output_grid[min_row, c] = key_color

            # 3. Propagate colors downwards starting from min_row + 1,
            #    but *only* fill if the original input pixel was background color.
            for r in range(min_row + 1, height):
                # Check the corresponding pixel in the *original input* grid
                if input_grid[r, c] == background_color:
                    # If it was background, fill it with the color from above in the *output* grid
                    output_grid[r, c] = output_grid[r - 1, c]
                # Else (if input_grid[r, c] was not background):
                #   The output_grid[r, c] already holds the correct value
                #   because output_grid was initialized as a copy of input_grid.
                #   So, no action is needed here.

        # If key color not in column, the column remains unchanged (already copied from input)

    return output_grid

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid based on the prioritized rules.
    """
    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    grid_shape = (height, width)

    # Define constants
    BACKGROUND_COLOR = 0
    KEY_COLOR = 2 # Red

    # --- Analyze Input Grid Properties ---
    unique_colors = find_unique_colors(input_np)
    other_colors = unique_colors - {BACKGROUND_COLOR, KEY_COLOR}
    # Determine the 'third_color' only if exactly 3 unique colors exist
    third_color = next(iter(other_colors), None) if len(unique_colors) == 3 else None
    num_unique_colors = len(unique_colors)

    # --- Rule Application Logic ---

    # 1. Check Rule 1: Solid Row Separation
    solid_row_index = find_solid_row(input_np, KEY_COLOR)
    # Rule 1 requires a solid key row AND exactly 3 unique colors
    if solid_row_index != -1 and third_color is not None:
        # Apply Rule 1
        output_grid = apply_row_separation(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color, solid_row_index)

    # 2. Check Rule 2: Fixed Diagonal Pattern Generation
    # Rule 2 requires NO solid key row, exactly 3 unique colors, AND all key pixels on specific diagonals
    elif solid_row_index == -1 and third_color is not None:
        all_key_on_diag = check_all_key_on_diag(input_np, KEY_COLOR)
        if all_key_on_diag:
            # Apply Rule 2
            output_grid = apply_fixed_pattern(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color)
        else:
            # Conditions for Rule 1 & 2 (diag part) not met, proceed to Rule 3
            output_grid = apply_column_filter_propagation(input_np, KEY_COLOR, BACKGROUND_COLOR)

    # 3. Apply Rule 3: Column Filter (Default)
    else:
        # Conditions for Rule 1 & 2 not met (e.g., not 3 colors, or rule 2 diag condition failed, or no solid row but not 3 colors)
        output_grid = apply_column_filter_propagation(input_np, KEY_COLOR, BACKGROUND_COLOR)

    # Convert final numpy array back to list of lists for the required output format
    return output_grid.tolist()