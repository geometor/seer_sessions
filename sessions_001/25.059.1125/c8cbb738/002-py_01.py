"""
Transforms a large input grid into a smaller output grid by:
1. Identifying the most frequent (dominant) color in the input.
2. Identifying all other colors (target colors).
3. Extracting an outer layer of non-dominant color pixels.
4. Forming the output grid using the extracted and filtered pixels, where background color is replaced.
"""

import numpy as np
from collections import Counter

def get_dominant_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def get_target_colors(grid, dominant_color):
    """Gets a set of colors in the grid, excluding the dominant color."""
    unique_colors = set(grid.flatten())
    unique_colors.remove(dominant_color)
    return unique_colors
    
def extract_outer_layer(grid, target_colors):
    """Extracts positions of pixels with target colors within the grid."""
    target_positions = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel in target_colors:
               target_positions.append((row_index, col_index, pixel))
    return target_positions

def reduce_to_MxM(positions):
  """Reduces the list of positions into M x M by sorting by row and taking top M"""
  # Sort by row
  positions.sort()
  # Calculate min and max values
  min_row, min_col, _ = positions[0]
  max_row, max_col, _ = positions[-1]
  height = max_row-min_row+1
  width = max_col-min_col+1
  size = max(height,width)

  rows = []
  row_values = []
  for r,c,p in positions:
    if r not in row_values:
      rows.append([])
      row_values.append(r)
    i = row_values.index(r)
    rows[i].append([r,c,p])
  
  for i in range(len(rows)):
    while len(rows[i]) > size:
      # find center
      dists = []
      for j in range(len(rows[i])):
        r, c, p = rows[i][j]
        dist = abs((min_col + max_col) / 2 - c)
        dists.append((dist, j))
      # remove the furthest away
      dists.sort(reverse=True)
      rows[i].pop(dists[0][1])

  # now flatten
  final_positions = []
  for i in range(len(rows)):
    for j in range(len(rows[i])):
      final_positions.append(rows[i][j])

  if len(final_positions) > size*size:
     final_positions = final_positions[:size*size]
  
  return size, final_positions

def create_output_grid(size, positions, dominant_color):
    """Creates the output grid based on extracted positions."""
    # initialize the output with all dominant
    output_grid = np.full((size, size), dominant_color)
    
    # find origin
    min_row = size -1
    min_col = size - 1

    for r,c,p in positions:
      if r < min_row:
        min_row = r
      if c < min_col:
        min_col = c
    # apply the values
    for r, c, p in positions:
        output_grid[r-min_row, c-min_col] = p

    return output_grid
    
def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Dominant Color
    dominant_color = get_dominant_color(input_grid)

    # 2. Identify Target Colors
    target_colors = get_target_colors(input_grid, dominant_color)

    # 3. Extract colored pixel layer positions
    target_positions = extract_outer_layer(input_grid, target_colors)

    # 4. Reduce to MxM and get new size
    size, reduced_positions = reduce_to_MxM(target_positions)

    # 5. Form Output Grid
    output_grid = create_output_grid(size, reduced_positions, dominant_color)

    return output_grid.tolist()