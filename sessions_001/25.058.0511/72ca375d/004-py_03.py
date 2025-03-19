import numpy as np
from scipy import ndimage

def object_details(grid, color):
    """Finds details of largest contiguous object of a given color."""
    labeled_grid, num_objects = ndimage.label(grid == color)
    if num_objects == 0:
        return None
    object_sizes = np.bincount(labeled_grid.ravel())
    largest_object_label = np.argmax(object_sizes[1:]) + 1
    rows, cols = np.where(labeled_grid == largest_object_label)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    size = height * width
    return {
        'color': color,
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'height': height,
        'width': width,
        'size': size
    }

def analyze_example(input_grid, output_grid):
  input_np = np.array(input_grid)
  output_np = np.array(output_grid)

  input_objects = []
  output_objects = []

  for color in range(10):
    input_details = object_details(input_np, color)
    if input_details:
      input_objects.append(input_details)
    output_details = object_details(output_np, color)
    if output_details:
      output_objects.append(output_details)


  return {
      'input': {'grid': input_grid, 'objects': input_objects},
      'output': {'grid': output_grid, 'objects': output_objects}
  }

example_data = []

example_data.append(analyze_example([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], [[6, 6, 6], [6, 6, 6], [6, 6, 6]]))
example_data.append(analyze_example([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[6, 6, 6, 6], [6, 6, 6, 6], [6, 6, 6, 6]]))
example_data.append(analyze_example([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[6, 6, 6, 6, 6], [6, 6, 6, 6, 6], [6, 6, 6, 6, 6]]))

for i, example in enumerate(example_data):
  print(f"Example {i}:")
  print(f"  Input Grid:\n{np.array(example['input']['grid'])}")
  print(f"  Output Grid:\n{np.array(example['output']['grid'])}")
  print(f"  Input Objects:")
  for obj in example['input']['objects']:
    print(f"    - Color: {obj['color']}, Size: {obj['size']}, Height: {obj['height']}, Width: {obj['width']}, Min Row: {obj['min_row']}, Min Col: {obj['min_col']}")
  print(f"  Output Objects:")
  for obj in example['output']['objects']:
    print(f"    - Color: {obj['color']}, Size: {obj['size']}, Height: {obj['height']}, Width: {obj['width']}, Min Row: {obj['min_row']}, Min Col: {obj['min_col']}")
