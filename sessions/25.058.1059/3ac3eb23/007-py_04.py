import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def compare_grids(grid1, grid2):
    """Compares two grids and returns the differences."""
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    else:
        return np.argwhere(grid1 != grid2)

def test_transform_on_examples(examples, transform_func):
    results = []
    for i, example in enumerate(examples):
      input_grid = np.array(example['input'])
      expected_output = np.array(example['output'])
      actual_output = transform_func(input_grid)
      diff_coords = compare_grids(expected_output, actual_output)
      diff_count = diff_coords.shape[0] if isinstance(diff_coords, np.ndarray) else 0

      results.append(
          {
              'example_index': i,
              'input_shape': input_grid.shape,
              'output_shape': expected_output.shape,
              'diff_count': diff_count,
              'diff_coords': diff_coords.tolist() if isinstance(diff_coords, np.ndarray) else diff_coords
          }
      )
    return results

# The following will be provided by the previous system messages
# train = [...] # the training examples list
# transform = ... # the python code for the transform function

# results = test_transform_on_examples(train, transform) # Call the testing function
# for result in results:
#     print(result)