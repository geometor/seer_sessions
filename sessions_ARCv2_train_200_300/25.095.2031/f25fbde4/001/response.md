```python
import math

"""
Scales a shape defined by non-zero elements (specifically value 4) within an input grid by a factor of 2, and crops the output to the scaled shape's bounding box.

1.  Identify all cells containing the value 4 in the input grid.
2.  Determine the minimum bounding box enclosing these cells.
3.  Create an output grid whose dimensions are twice the height and width of the input bounding box, initialized with zeros.
4.  For each input cell containing 4 within the bounding box, map it to a 2x2 block of 4s in the output grid, based on its relative position within the input bounding box.
5.  Return the resulting output grid.
"""

def find_shape_coords(grid: list[list[int]], target_value: int) -> list[tuple[int, int]]:
    """Finds the coordinates of all cells with the target value."""
    coords = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == target_value:
                coords.append((r, c))
    return coords

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the bounding box of the given coordinates.
    Returns (min_row, min_col, height, width).
    Returns (0, 0, 0, 0) if coords is empty.
    """
    if not coords:
        return 0, 0, 0, 0 # Or raise an error, depending on desired behavior for empty shapes

    min_row = min(r for r, c in coords)
    max_row = max(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_col = max(c for r, c in coords)

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return min_row, min_col, height, width


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the 2x scaling and cropping transformation to the input grid.
    """
    shape_value = 4
    background_value = 0
    scale_factor = 2

    # 1. Identify all cells containing the shape value (4).
    shape_coords = find_shape_coords(input_grid, shape_value)

    # Handle case where no shape is found
    if not shape_coords:
        return [] # Return an empty grid as per examples potentially implying this

    # 2. Determine the minimum bounding box for the shape cells.
    min_row, min_col, bb_height, bb_width = calculate_bounding_box(shape_coords)

    # 3. Calculate output grid dimensions and initialize it with the background value.
    out_height = bb_height * scale_factor
    out_width = bb_width * scale_factor
    output_grid = [[background_value for _ in range(out_width)] for _ in range(out_height)]

    # 4. Iterate through the shape coordinates and place the scaled 2x2 blocks.
    for r, c in shape_coords:
        # Calculate relative coordinates within the input bounding box
        rel_r = r - min_row
        rel_c = c - min_col

        # Calculate the top-left corner for the 2x2 block in the output grid
        out_r_start = rel_r * scale_factor
        out_c_start = rel_c * scale_factor

        # 5. Fill the 2x2 block in the output grid with the shape value.
        for i in range(scale_factor):
            for j in range(scale_factor):
                # Check bounds just in case, although logic should prevent out-of-bounds
                if 0 <= out_r_start + i < out_height and 0 <= out_c_start + j < out_width:
                     output_grid[out_r_start + i][out_c_start + j] = shape_value

    # 6. Return the generated output grid.
    return output_grid
```