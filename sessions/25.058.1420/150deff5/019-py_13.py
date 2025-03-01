import numpy as np

def describe_shape(shape_coords):
    """Provides a description of a shape's properties."""
    if not shape_coords:
        return "No shape"

    rows, cols = zip(*shape_coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return f"Height: {height}, Width: {width}, Top-left: ({min_row}, {min_col}), Bottom-right: ({max_row}, {max_col})"

def analyze_results(task):
  print(f"Task: {task['name']}")
  for i, pair in enumerate(task['train']):
    input_grid = np.array(pair['input'])
    output_grid = np.array(pair['output'])
    predicted_output = transform(input_grid)
    
    shapes_in = find_shapes(input_grid, 5)
    shapes_out = find_shapes(output_grid, 5)
    
    print(f"  Example {i+1}:")
    print(f"    Input shapes: {len(shapes_in)}")
    for j, shape in enumerate(shapes_in):
        print(f"      Shape {j+1}: {describe_shape(shape)}")
        
    print(f"    Output shapes: {len(shapes_out)}")

    if np.array_equal(output_grid, predicted_output):
        print("    Prediction: Correct")
    else:
        print("    Prediction: Incorrect")
        diff = output_grid != predicted_output
        print("differences")
        print(np.argwhere(diff))
        print(output_grid[diff])
        print(predicted_output[diff])


# Example Usage (replace with actual task data):
task1 = {
    'name': 'Example Task',
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0],
                   [0, 5, 5, 5, 5, 5, 0],
                   [0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 2, 2, 8, 8, 0],
                    [0, 0, 0, 0, 0, 0, 0]]},

        {'input': [[0, 0, 0, 0, 0, 0, 0],
                   [0, 5, 5, 5, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 2, 8, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]]},

       {'input':  [[0, 0, 5, 0, 0, 0, 0],
                   [0, 0, 5, 0, 0, 0, 0],
                   [0, 0, 5, 0, 0, 0, 0],
                   [0, 0, 5, 0, 0, 5, 0],
                   [0, 0, 5, 0, 0, 5, 0],
                   [0, 0, 0, 0, 0, 5, 0],
                   [0, 0, 0, 0, 0, 0, 0]],

        'output': [[0, 0, 2, 0, 0, 0, 0],
                   [0, 0, 2, 0, 0, 0, 0],
                   [0, 0, 8, 0, 0, 0, 0],
                   [0, 0, 2, 0, 0, 2, 0],
                   [0, 0, 8, 0, 0, 8, 0],
                   [0, 0, 0, 0, 0, 8, 0],
                   [0, 0, 0, 0, 0, 0, 0]]}
    ]
}

analyze_results(task1)
