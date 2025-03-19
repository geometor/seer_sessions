import numpy as np

# Example data (replace with actual data from the ARC task)
# Simulating with simplified data for demonstration
# You'd replace this with the real input/output grids for each training example
training_examples = [
    (
        np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]]),  # Input 0
        np.array([[1, 1, 0], [1, 1, 0], [1, 1, 0]]),  # Expected Output 0
    ),
    (
        np.array([[0, 0, 6], [0, 6, 0], [6, 0, 0]]),  # Input 1
        np.array([[0, 6, 6], [6, 6, 0], [6, 0, 0]]),  # Expected Output 1
    ),
    (
        np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),  # Input 2
        np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),  # Expected Output 2
    ),
 (
        np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0],[0, 0, 6, 0, 0], [0, 0, 6, 0, 0]]),  # Input 3
        np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0],[0, 6, 6, 0, 0], [6, 6, 0, 0, 0]]),  # Expected Output 3
    ),
]

def calculate_metrics(input_grid, expected_output, predicted_output):
  """Calculates metrics for a single example."""

  input_objects = {}
  expected_objects = {}
  predicted_objects = {}

  for color in range(10):
    input_objects[color] = np.sum(input_grid == color)
    expected_objects[color] = np.sum(expected_output == color)
    predicted_objects[color] = np.sum(predicted_output == color)

  accuracy = np.sum(predicted_output == expected_output) / expected_output.size

  return input_objects, expected_objects, predicted_objects, accuracy

# Previous transform function goes here.
# find_objects
# extend_object

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # change output pixels based on rules
    for color, object_pixels in objects:
        if color == 5: #gray
            continue #do nothing
        elif color in (1,6):  #azure or magenta

            extended_objects = extend_object(object_pixels, color)

            # Add extended object to the output
            for ext_color, ext_pixels in extended_objects:
               for r, c in ext_pixels:
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = ext_color

    return output_grid


all_metrics = []
for i, (input_grid, expected_output) in enumerate(training_examples):
    predicted_output = transform(input_grid)
    metrics = calculate_metrics(input_grid, expected_output, predicted_output)
    all_metrics.append((i, metrics))

for i, metrics in all_metrics:
    input_objects, expected_objects, predicted_objects, accuracy = metrics
    print(f"Example {i+1}:")
    print(f"  Input Objects: {input_objects}")
    print(f"  Expected Objects: {expected_objects}")
    print(f"  Predicted Objects: {predicted_objects}")
    print(f"  Accuracy: {accuracy:.4f}")
    print("-" * 20)