import numpy as np

def get_object_extents(grid, color):
    """Finds the top-left and bottom-right coordinates of an object."""
    rows, cols = grid.shape
    pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
              pixels.append((r,c))

    if len(pixels) == 0:
        return None, None

    min_row = min(pixels, key=lambda p: p[0])[0]
    max_row = max(pixels, key=lambda p: p[0])[0]
    min_col = min(pixels, key=lambda p: p[1])[1]
    max_col = max(pixels, key=lambda p: p[1])[1]
    
    return (min_row, min_col), (max_row, max_col)

def describe_object(grid, color):
    """Describes an object's properties."""
    top_left, bottom_right = get_object_extents(grid, color)

    if top_left is None:
        return f"No {color_name(color)} object found."

    width = bottom_right[1] - top_left[1] + 1
    height = bottom_right[0] - top_left[0] + 1
    return f"{color_name(color)} object: Top-left: {top_left}, Bottom-right: {bottom_right}, Width: {width}, Height: {height}"

def color_name(value):
  """ convert color value 0-9 to the name"""
  color_names = {
    0: "black",
    1: "blue",
    2: "red",
    3: "green",
    4: "yellow",
    5: "gray",
    6: "magenta",
    7: "orange",
    8: "azure",
    9: "maroon"
  }
  return color_names.get(value,"unknown")

def analyze_grid(grid, label):
  print(f"--- {label} ---")
  print(grid)
  for color in range(10):  # Check all colors
      description = describe_object(grid, color)
      if "No object" not in description:
          print(description)

def find_object(grid, color, has_inner_color=None):
    """Finds an object of the specified color, optionally with an inner color."""
    rows, cols = grid.shape
    top_left = None
    bottom_right = None
    inner_pixels = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                if top_left is None:
                    top_left = (r, c)
                bottom_right = (r, c)

                if has_inner_color: # check the neighbors if inner_color requested
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            nr, nc = r + i, c + j
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == has_inner_color:
                                inner_pixels.append((nr, nc))
    if top_left is not None:
     if has_inner_color is None or len(inner_pixels) > 0: # must contain inner pixel
        return top_left, bottom_right, inner_pixels
     else:
        return None, None, []
    
    return None, None, []
    

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the blue shape with a yellow pixel inside.
    blue_top, blue_bottom, inner_yellow = find_object(input_grid, 1, has_inner_color=4)

    # Find the azure shape.
    azure_top, azure_bottom, _ = find_object(input_grid, 8)

    # Find the yellow shape
    yellow_top, yellow_bottom, _ = find_object(input_grid, 4)
    
    if blue_top is None or azure_top is None or yellow_top is None:
        return output_grid # return the copy if not all objects are found

    # Combine azure and yellow shapes' bounding boxes.
    combined_top = (min(azure_top[0], yellow_top[0]), min(azure_top[1], yellow_top[1]))
    combined_bottom = (max(azure_bottom[0], yellow_bottom[0]), max(azure_bottom[1], yellow_bottom[1]))

    # Expand the combined shape.
    expanded_top = (combined_top[0]-1, combined_top[1]-1)
    expanded_bottom = (combined_bottom[0]+1, combined_bottom[1]+1)

    # Fill the expanded area with azure, keeping the inner yellow.
    for r in range(expanded_top[0], expanded_bottom[0] + 1):
        for c in range(expanded_top[1], expanded_bottom[1] + 1):
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r, c] = 8
    
    # paint over with the original yellow from the bottom
    for r in range(yellow_top[0], yellow_bottom[0] + 1):
        for c in range(yellow_top[1], yellow_bottom[1] + 1):
             output_grid[r, c] = 4

    # fill above area with azure
    for r in range(0, expanded_top[0]):
        for c in range(0, output_grid.shape[1]):
          output_grid[r,c] = 0 # fill the top
    for r in range(0, expanded_top[0]):
      for c in range(combined_top[1]-1, combined_bottom[1]+2):
        output_grid[r,c] = 8 # paint with azure from column of expanded top

    return output_grid

# dummy grids
grids = {
'input_0': np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 4, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
'output_0': np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 4, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
'input_1': np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0]]),
'output_1': np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 4, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8]]),
'input_2': np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4]]),
'output_2': np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 4, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 1, 1, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4]])
}

for label, grid in grids.items():
  analyze_grid(grid, label)
  if 'input' in label:
      output = transform(grid)
      analyze_grid(output, f"result for {label}")