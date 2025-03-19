import numpy as np

def object_properties(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # No object of that color

    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return {
        'color': color,
        'min_row': min_row,
        'min_col': min_col,
        'height': height,
        'width': width,
        'coords': coords
    }

def analyze_example(input_grid, output_grid):
    input_objects = []
    output_objects = []

    for color in np.unique(input_grid):
        props = object_properties(input_grid, color)
        if props:
            input_objects.append(props)

    for color in np.unique(output_grid):
        props = object_properties(output_grid, color)
        if props:
            output_objects.append(props)
            
    return {
      'input_grid_shape': input_grid.shape,
      'output_grid_shape': output_grid.shape,
      'input_objects': input_objects,
      'output_objects': output_objects
    }

def report(task_examples):
    analysis = []
    for i, (input_grid, output_grid) in enumerate(task_examples):
        example_analysis = analyze_example(input_grid, output_grid)
        analysis.append(f"--- Example {i+1} ---")
        analysis.append(f"Input Shape: {example_analysis['input_grid_shape']}")
        analysis.append(f"Output Shape: {example_analysis['output_grid_shape']}")
        analysis.append("Input Objects:")
        for obj in example_analysis['input_objects']:
            analysis.append(f"  - Color: {obj['color']}, Top-Left: ({obj['min_row']},{obj['min_col']}), Size: {obj['height']}x{obj['width']}")
        analysis.append("Output Objects:")
        for obj in example_analysis['output_objects']:
            analysis.append(f"  - Color: {obj['color']}, Top-Left: ({obj['min_row']},{obj['min_col']}), Size: {obj['height']}x{obj['width']}")
    return "\n".join(analysis)
# get the examples from the environment - the 'task' variable
examples = task.train
task_examples = [(np.array(eg['input']), np.array(eg['output'])) for eg in examples]

print(report(task_examples))
