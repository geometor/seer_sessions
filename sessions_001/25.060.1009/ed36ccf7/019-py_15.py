import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes a single example and returns relevant metrics."""

    def get_object_details(grid):
        """Finds details of the object with color 9."""
        coords = np.argwhere(grid == 9)
        if coords.size == 0:
            return None, None, None, None
        min_row, min_col = coords.min(axis=0)
        max_row, max_col = coords.max(axis=0)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        return coords, (min_row, min_col), (height, width), (max_row, max_col)

    input_coords, input_top_left, input_dims, input_bottom_right = get_object_details(input_grid)
    output_coords, output_top_left, output_dims, output_bottom_right = get_object_details(output_grid)
    predicted_coords, predicted_top_left, predicted_dims, predicted_bottom_right = get_object_details(predicted_output)

    if input_coords is None:
      input_shape = "None"
    elif input_dims == (2,2):
      input_shape = "Square"
    elif input_dims == (3,2) or input_dims == (2,3):
      input_shape = "L"
    else:
       input_shape = "Other"

    if output_coords is None:
      output_shape = "None"
    elif output_dims == (2,2):
      output_shape = "Square"
    elif output_dims == (3,2) or output_dims == (2,3):
      output_shape = "L"
    else:
      output_shape = "Other"
    
    if predicted_coords is None:
      predicted_shape = "None"
    elif predicted_dims == (2,2):
      predicted_shape = "Square"
    elif predicted_dims == (3,2) or predicted_dims == (2,3):
      predicted_shape = "L"
    else:
      predicted_shape = "Other"

    return {
        "input_object_exists": input_coords is not None,
        "input_top_left": input_top_left,
        "input_dimensions": input_dims,
        "input_shape": input_shape,
        "input_bottom_right": input_bottom_right,
        "output_object_exists": output_coords is not None,
        "output_top_left": output_top_left,
        "output_dimensions": output_dims,
        "output_shape": output_shape,
        "output_bottom_right": output_bottom_right,
        "predicted_object_exists": predicted_coords is not None,
        "predicted_top_left": predicted_top_left,
        "predicted_dimensions": predicted_dims,
        "predicted_shape": predicted_shape,
        "predicted_bottom_right": predicted_bottom_right,
        "output_matches_predicted": np.array_equal(output_grid, predicted_output)
    }

# Example Usage (assuming you have your input_grid, output_grid, and predicted_output for each example)
# Replace these with your actual data
example_results = []

task_id = '6d75e8bb'

#load grids
import json
with open('data/training/'+task_id+'.json', 'r') as f:
  task = json.load(f)

train_examples = task['train']
for i, ex in enumerate(train_examples):
    input_grid = np.array(ex['input'])
    output_grid = np.array(ex['output'])
    predicted_output = transform(input_grid)
    analysis = analyze_example(input_grid, output_grid, predicted_output)
    example_results.append( (i, analysis))

for i, result in example_results:
   print(f'Example {i}:')
   print(result)
