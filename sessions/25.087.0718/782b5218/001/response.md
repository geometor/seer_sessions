```python
import numpy as np

"""
This program transforms an input grid based on the arrangement of a 'key color' (red=2) and the presence of other colors. 

The transformation follows these prioritized rules:

1.  **Solid Row Rule:** If a horizontal row consists entirely of the key color (red=2), this row acts as a separator. The output grid will have this separator row preserved. All rows above it are filled with the background color (white=0). All rows below it are filled with the 'third color' present in the input grid (if one exists).

2.  **Fixed Diagonal Pattern Rule:** If Rule 1 does not apply, and the input grid contains exactly three distinct colors (background=0, key=2, and a third color), the output grid is constructed with a fixed diagonal pattern. A band two pixels thick diagonally (specifically, cells where row == col + 1 or row == col + 2) is filled with the key color (red=2). The area below this band (row > col + 2) is filled with the third color. The area above the band (row < col + 1) is filled with the background color (white=0).

3.  **Column Filter Rule:** If neither Rule 1 nor Rule 2 applies, a column-wise filter is applied. For each column, the highest occurrence of the key color (red=2) is identified. All pixels in that column *above* this highest key color pixel are changed to the background color (white=0). Pixels at or below the highest key color pixel, and pixels in columns containing no key color, remain unchanged from the input.
"""

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

def apply_row_separation(grid_shape, key_color, background_color, third_color, solid_row_index):
    """Applies Rule 1: Row Separation."""
    height, width = grid_shape
    output_grid = np.full(grid_shape, background_color, dtype=int) # Fill above with background initially
    
    if solid_row_index < height -1 :
         # Fill below with third color
        output_grid[solid_row_index + 1:, :] = third_color
   
    # Set the separator row
    output_grid[solid_row_index, :] = key_color

    return output_grid

def apply_fixed_pattern(grid_shape, key_color, background_color, third_color):
    """Applies Rule 2: Fixed Diagonal Pattern."""
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
            # else: output_grid[r, c] = background_color

    return output_grid

def apply_column_filter(grid, key_color, background_color):
    """Applies Rule 3: Column Filtering."""
    height, width = grid.shape
    output_grid = np.copy(grid) # Start with a copy of the input

    for c in range(width):
        # Find the row index of the highest occurrence of the key color in the column
        key_color_indices = np.where(grid[:, c] == key_color)[0]
        if len(key_color_indices) > 0:
            min_row = np.min(key_color_indices)
            # Set pixels above the highest key color to background
            output_grid[:min_row, c] = background_color
        # If key color not in column, the column remains unchanged (already copied)

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    grid_shape = (height, width)

    BACKGROUND_COLOR = 0
    KEY_COLOR = 2

    # 1. Analyze Input
    unique_colors = find_unique_colors(input_np)
    other_colors = unique_colors - {BACKGROUND_COLOR, KEY_COLOR}
    third_color = next(iter(other_colors)) if len(other_colors) == 1 else None # Assign if exactly one other color exists
    num_unique_colors = len(unique_colors)

    # 2. Check for Solid Key Color Row (Rule 1)
    solid_row_index = find_solid_row(input_np, KEY_COLOR)
    if solid_row_index != -1 and third_color is not None: # Rule 1 needs a third color to fill below
        # print(f"Applying Rule 1: Solid row at {solid_row_index}, third_color={third_color}")
        output_grid = apply_row_separation(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color, solid_row_index)

    # 3. Check for Three Colors & Fixed Pattern Rule (Rule 2)
    elif solid_row_index == -1 and num_unique_colors == 3 and third_color is not None:
        # print(f"Applying Rule 2: Three colors found ({BACKGROUND_COLOR}, {KEY_COLOR}, {third_color})")
        output_grid = apply_fixed_pattern(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color)

    # 4. Apply Column Filter Rule (Rule 3 - Default)
    else:
        # print("Applying Rule 3: Column Filter")
        output_grid = apply_column_filter(input_np, KEY_COLOR, BACKGROUND_COLOR)

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```