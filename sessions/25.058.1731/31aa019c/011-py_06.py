import numpy as np

def describe_subgrid(grid):
    """Finds and describes a 3x3 subgrid with a differently colored center."""
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            subgrid = grid[i:i+3, j:j+3]
            center_color = subgrid[1, 1]
            outer_colors = subgrid.flatten()
            outer_colors = outer_colors[outer_colors != center_color]
            if len(outer_colors) > 0 and np.all(outer_colors == outer_colors[0]):
                #all outer colors are the same, and different from the center
                return {
                    "row_start": i,
                    "col_start": j,
                    "center_color": center_color,
                    "outer_color": outer_colors[0],
                    'subgrid': subgrid
                }
    return None

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_desc = describe_subgrid(input_grid)
    output_desc = describe_subgrid(output_grid)

    if input_desc is not None and output_desc is not None:

        return {
            "input_subgrid_location": (input_desc["row_start"], input_desc["col_start"]),
            "input_center_color": input_desc["center_color"],
            "input_outer_color": input_desc["outer_color"],
            "output_subgrid_location": (output_desc["row_start"], output_desc["col_start"]),
            "output_center_color": output_desc["center_color"],
            "output_outer_color": output_desc["outer_color"],
            'input_subgrid': input_desc['subgrid'],
            'output_subgrid': output_desc['subgrid']
        }
    else:
      if(input_desc == None):
        return {'error': 'no input'}
      else:
        return {'error': 'no output'}
    return None

# Example usage (assuming input_grids and output_grids are lists of numpy arrays)
task_data = {
  'train': [
    {
      'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 5, 1, 5], [0, 0, 0, 0, 0, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 2, 6, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
     {
      'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 3, 1, 3, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 2, 6, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
      'input': np.array([[8, 8, 8, 0, 0, 0, 0, 0, 0, 0], [8, 1, 8, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 2, 6, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }
  ]
}

results = [analyze_example(example['input'], example['output']) for example in task_data['train']]
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    if 'error' in result:
        print(f"  Error: {result['error']}")
    else:
        print(f"  Input Subgrid Location: {result['input_subgrid_location']}")
        print(f"  Input Center Color: {result['input_center_color']}")
        print(f"  Input Outer Color: {result['input_outer_color']}")
        print(f"  Output Subgrid Location: {result['output_subgrid_location']}")
        print(f"  Output Center Color: {result['output_center_color']}")
        print(f"  Output Outer Color: {result['output_outer_color']}")
        print(f"  Input subgrid:\n {result['input_subgrid']}")
        print(f"  Output subgrid:\n {result['output_subgrid']}")