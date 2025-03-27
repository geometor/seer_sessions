```python
import numpy as np

"""
Identify all 4x4 'solid' (all same non-white color) and 'hollow' (border same non-white color, center white) squares in the input grid.
Sort the hollow squares by their original top-to-bottom, left-to-right position.
Sort the solid squares similarly.
Create an output grid with width 8 and height 4 * max(number_of_hollow, number_of_solid).
Place the sorted hollow squares down the left columns (0-3) of the output grid.
Place the sorted solid squares down the right columns (4-7) of the output grid.
Pad any remaining space at the bottom of either column with white (0).
"""

def is_solid_square(block):
    """Checks if a 4x4 numpy array is a solid square (all same non-white color)."""
    if block.shape != (4, 4):
        return False, -1
    first_pixel = block[0, 0]
    if first_pixel == 0: # Solid squares cannot be white
        return False, -1
    # Check if all pixels are the same as the first pixel
    if np.all(block == first_pixel):
        return True, first_pixel
    return False, -1

def is_hollow_square(block):
    """Checks if a 4x4 numpy array is a hollow square (border same non-white, center white)."""
    if block.shape != (4, 4):
        return False, -1
    # Check inner 2x2 square is white (0)
    inner_block = block[1:3, 1:3]
    if not np.all(inner_block == 0):
        return False, -1

    # Check border pixels
    border_pixels = np.concatenate([
        block[0, :],         # Top row
        block[-1, :],        # Bottom row
        block[1:-1, 0],    # Left column (excluding corners)
        block[1:-1, -1]    # Right column (excluding corners)
    ])

    if border_pixels.size != 12: # Should be exactly 12 border pixels
         return False, -1

    first_border_pixel = border_pixels[0]
    if first_border_pixel == 0: # Border color cannot be white
        return False, -1

    # Check if all border pixels are the same non-white color
    if np.all(border_pixels == first_border_pixel):
        return True, first_border_pixel
    return False, -1

def transform(input_grid):
    """
    Finds solid and hollow 4x4 squares, sorts them, and arranges them
    into two columns in the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    hollow_squares = []
    solid_squares = []

    # Scan the input grid for 4x4 squares
    for r in range(height - 3):
        for c in range(width - 3):
            block = input_np[r:r+4, c:c+4]
            
            # Check if it's a hollow square
            is_hollow, _ = is_hollow_square(block)
            if is_hollow:
                hollow_squares.append({'block': block, 'pos': (r, c)})
                # Optimization: If a square is found, skip the next 3 columns/rows
                # This assumes non-overlapping squares as observed in examples.
                # If overlap was possible, this optimization would be invalid.
                # c += 3 # Be careful if squares could potentially overlap near edges
                continue # A block can't be both hollow and solid

            # Check if it's a solid square
            is_solid, _ = is_solid_square(block)
            if is_solid:
                solid_squares.append({'block': block, 'pos': (r, c)})
                # c += 3 # Same optimization note as above

    # Sort squares based on position (top-to-bottom, then left-to-right)
    hollow_squares.sort(key=lambda x: (x['pos'][0], x['pos'][1]))
    solid_squares.sort(key=lambda x: (x['pos'][0], x['pos'][1]))

    # Determine output grid dimensions
    num_hollow = len(hollow_squares)
    num_solid = len(solid_squares)
    output_height = max(num_hollow, num_solid) * 4
    output_width = 8

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place hollow squares in the left column
    for i, square_info in enumerate(hollow_squares):
        start_row = i * 4
        output_grid[start_row:start_row+4, 0:4] = square_info['block']

    # Place solid squares in the right column
    for i, square_info in enumerate(solid_squares):
        start_row = i * 4
        output_grid[start_row:start_row+4, 4:8] = square_info['block']

    # Convert numpy array back to list of lists for the expected output format
    return output_grid.tolist()

```