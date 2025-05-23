"""
The transformation rearranges the pixels of the input grid to form the output grid.
The rearrangement logic is complex, but preserves most pixel color counts.
Pixels appear to be reordered based on a process to be determined, not a simple geometric transformation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into the output grid by rearranging pixels.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Create a list of pixel coordinates and colors
    pixels = []
    for r in range(rows):
        for c in range(cols):
            pixels.append(((r, c), input_grid[r, c]))

    # Sort pixels by color, prioritizing colors that undergo changes.
    #   This part is a best guess, anticipating some swapping logic.
    #   Order of colors may need adjustment after further analysis of examples.
    pixels.sort(key=lambda x: (x[1] != 8, x[1] != 2, x[1] != 4, x[1] != 1, x[1]))

    # Build the output grid. Use a mapping or a shuffling-based approach.
    # The exact mapping isn't yet known, so for now, we're just placing
    #   pixels in a new grid, but it's not the correct final order.
    output_pixels = [] #store the pixel after the re-arrangment.
    
    # Start by processing pixels other than '8' and '2'.
    # Focus on handling the changes first, to deduce any possible substitution rules.
    
    # initialize the index for the pixel list
    pixel_index = 0

    for r in range(rows):
      for c in range(cols):
        output_pixels.append(((r,c), pixels[pixel_index][1]))
        pixel_index += 1
        pixel_index = pixel_index % len(pixels) # wrap around the list.

    # now build final output with reordered pixel
    for pixel in output_pixels:
        output_grid[pixel[0]] = pixel[1]


    return output_grid