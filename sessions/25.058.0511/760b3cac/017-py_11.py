import numpy as np

def analyze_shapes(input_grid, output_grid):
    """Analyzes the azure and yellow shapes in the input and output grids."""

    def get_shape_info(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return None
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)
        width = max_col - min_col + 1
        height = max_row - min_row + 1
        size = width * height
        return {
            'min_row': min_row,
            'max_row': max_row,
            'min_col': min_col,
            'max_col': max_col,
            'width': width,
            'height': height,
            'size': size,
            'coords': coords
        }

    azure_input = get_shape_info(input_grid, 8)
    azure_output = get_shape_info(output_grid, 8)
    yellow_input = get_shape_info(input_grid, 4)
    yellow_output = get_shape_info(output_grid, 4) # should be the same as input

    return {
        'azure_input': azure_input,
        'azure_output': azure_output,
        'yellow_input': yellow_input,
        'yellow_output': yellow_output
    }

def array_to_string(array):
    return np.array2string(array, separator=',', formatter={'int':lambda x: f'{x:d}'})
# Example usage (replace with actual input/output grids)
# results = analyze_shapes(input_grid, output_grid)
# print(results)

# Now, loop through the examples from the problem
task_id = '7b60105d' # from prompt
examples = [
    {
        "input": array_to_string(np.array([[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])),
        "output": array_to_string(np.array([[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])),
    },
    {
        "input": array_to_string(np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,4,4,4,4,0,0,0,0],[0,0,0,0,0,0,4,4,4,4,0,0,0,0],[0,0,0,0,8,8,8,8,8,8,0,0,0,0],[0,0,0,0,8,8,8,8,8,8,0,0,0,0],[0,0,0,0,8,8,8,8,8,8,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])),
        "output": array_to_string(np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,0,0,0,0,4,4,4,4,0,0,0,0],[0,0,0,0,0,0,4,4,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]])),
    },
    {
        "input": array_to_string(np.array([[0,0,0,0,0,0,0,0,0,0,0],[0,4,4,0,0,0,0,0,0,0,0],[0,4,4,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]])),
        "output": array_to_string(np.array([[0,4,4,0,0,0,0,0,0,0,0],[0,4,4,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,8,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]])),
    },
]

for i, ex in enumerate(examples):
    input_grid = np.array(eval(ex['input']))
    output_grid = np.array(eval(ex['output']))
    results = analyze_shapes(input_grid, output_grid)
    print(f"Example {i+1}:")
    print(results)