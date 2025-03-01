import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    errors = np.sum(output_grid != predicted_grid)
    input_objects = {}
    output_objects = {}

    for color in np.unique(input_grid):
        input_objects[color] = np.argwhere(input_grid == color).shape[0]
    for color in np.unique(output_grid):
        output_objects[color] = np.argwhere(output_grid == color).shape[0]

    return {
        "errors": errors,
        "input_objects": input_objects,
        "output_objects": output_objects
    }

# Dummy data for demonstration - replace with actual data
task = {
   'train': [
      {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 8, 0, 0, 2], [2, 0, 0, 8, 8, 8, 0, 2], [2, 0, 0, 0, 8, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2]]},
      {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 8, 8, 0, 0, 2], [2, 0, 8, 8, 8, 8, 0, 2], [2, 0, 0, 8, 8, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2]]},
      {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 0, 2], [2, 2, 2, 2, 2, 2, 2, 2]]}
   ]
}

for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_grid = transform(input_grid)  # Assuming 'transform' is your function
    analysis = analyze_example(input_grid, output_grid, predicted_grid)
    print(f"Example {i+1}:")
    print(f"  Errors: {analysis['errors']}")
    print(f"  Input Objects: {analysis['input_objects']}")
    print(f"  Output Objects: {analysis['output_objects']}")
    print(f"  Predicted vs Expected Output:")
    print(f"  Predicted:\n{predicted_grid}")
    print(f"Output:\n{output_grid}")
