"""
1.  **Identify the azure vertical line:** Find the vertical line of connected pixels with the color '8' (azure). It may not always be straight, and may change position and size.

2.  **Locate object stripes:** Starting from the azure vertical line, locate the sets of adjacent horizontal pixels of the same color (excluding azure) on both the left and the right. We identify each set of horizontal pixels with the same color as a stripe.

3. **Iterate each object stripe**: For each identified stripe:
    * Iterate from top to buttom.
    * Get the color of the lowest element of the stripe.
    * Iterate from left to right.
    * If it is the top or buttom row, set the color to the lowest color of that stripe.

4.  **Produce Output:** The modified grid, with the specified changes, becomes the output.
"""

import numpy as np

def find_azure_line(grid):
    """Finds the 'azure' (8) vertical line, handling potential variations."""
    azure_lines = []
    rows, cols = grid.shape
    for c in range(cols):
      current_line = []
      for r in range(rows):
        if grid[r,c] == 8:
          current_line.append((r,c))
        else:
          if len(current_line) > 0:
            azure_lines.append(current_line)
          current_line = []
      if len(current_line) > 0:
            azure_lines.append(current_line)
    
    #find longest line
    longest_line = []
    for line in azure_lines:
      if len(line) > len(longest_line):
        longest_line = line

    return longest_line

def get_object_stripes(grid, azure_line):
    """Identifies object stripes to the left and right of the azure line."""
    rows, cols = grid.shape
    stripes = []

    # Convert azure_line to a set for faster lookup
    azure_line_set = set(azure_line)

    for r in range(rows):
        current_stripe = []
        for c in range(cols):
            if (r, c) not in azure_line_set:
                if len(current_stripe) == 0 or grid[r, c] == current_stripe[-1][2]:  # Same color, continue stripe
                    current_stripe.append((r, c, grid[r, c]))
                else:  # Different color, end current stripe and start a new one
                    if current_stripe[-1][2] != 8 and len(current_stripe) > 0:  #exclude azure
                      stripes.append(current_stripe)
                    current_stripe = [(r, c, grid[r, c])]  # Start new stripe
            elif len(current_stripe) > 0: # we are at azure, end the stripe
              if current_stripe[-1][2] != 8 and len(current_stripe) > 0:  #exclude azure
                stripes.append(current_stripe)
              current_stripe = []

        if len(current_stripe) > 0 and current_stripe[-1][2] != 8:  # Check for stripe at the end of the row
              stripes.append(current_stripe)


    return stripes


def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # change output pixels 
    azure_line = find_azure_line(grid)
    object_stripes = get_object_stripes(grid, azure_line)

    for stripe in object_stripes:
      #find the vertical bounds
      top_row = min([pixel[0] for pixel in stripe])
      buttom_row = max([pixel[0] for pixel in stripe])

      #get lowest color
      replacement_color = stripe[-1][2]

      #replace top and buttom
      for x,y,color in stripe:
        if x == top_row or x == buttom_row:
          output_grid[x,y] = replacement_color
    

    return output_grid.tolist()