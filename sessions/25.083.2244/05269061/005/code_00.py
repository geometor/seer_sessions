"""
1. Identify Background: Determine the background color. This might be the color '0', or the most frequent color in the input grid.
2. Copy Input: Create a copy of the entire input grid.
3. Fill Background: Replace all colors in the output grid other than the core colors with the identified background color.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Determines the background color based on frequency."""
    # Flatten the grid and count color occurrences
    color_counts = Counter(grid.flatten())
    # Return the most common color
    most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

def transform(input_grid):
    """Transforms the input grid by filling the background."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Copy the input grid

    # 1. Identify Background
    background_color = get_background_color(input_grid)

    # 3. Fill Background (No need to find "core colors", we fill everything *except* background)
    # Iterate through the grid
    rows, cols = input_grid.shape

    # Identify Non-Background
    non_background_colors = [color for color in np.unique(input_grid) if color != background_color ]
    
    if len(non_background_colors) > 0:
      non_background = non_background_colors[0] #assume only one "non background"
      for r in range(rows):
        for c in range(cols):
          if output_grid[r,c] != non_background:
              output_grid[r,c] = background_color


    return output_grid.tolist()