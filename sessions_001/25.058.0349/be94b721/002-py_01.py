"""
1.  **Identify the Red Region:** Locate the contiguous region of red (2) pixels within the input grid.
2.  **Extract Red Region:** Isolate this red region, discarding all other colored pixels.
3. **Crop:** remove the surrounding white space pixels and keep the largest block of red.
4.  **Form Output:** The cropped red region constitutes the output grid.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None
    # Compute the bounding box.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    return (min_row, max_row, min_col, max_col), coords

def extract_region(grid, coords):
  # create a mask
  mask = np.zeros_like(grid, dtype=bool)
  for r, c in coords:
    mask[r,c] = True
  return mask

def crop_region(grid, bbox):
    # Crop the grid to the bounding box.
    min_row, max_row, min_col, max_col = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the bounding box and coordinates of the red region.
    red_bbox, red_coords = find_object(input_grid, 2)

    if red_bbox is None:
        return []

    # Extract the red region using the mask.
    red_mask = extract_region(input_grid, red_coords)
    red_region = np.where(red_mask, input_grid, 0)

    # Crop the red region.
    cropped_red_region = crop_region(red_region, red_bbox)

    return cropped_red_region.tolist()