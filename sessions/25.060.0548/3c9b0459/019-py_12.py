def get_grid_properties(grid):
    """
    Calculates properties of a given grid.
    """
    n = len(grid)
    m = len(grid[0]) if n > 0 else 0
    unique_colors = set()
    for row in grid:
        for cell in row:
            unique_colors.add(cell)
    num_unique_colors = len(unique_colors)
    
    return {
      'height': n,
      'width': m,
      'unique_colors': sorted(list(unique_colors)),
      'num_unique_colors': num_unique_colors
    }

def analyze_examples(task_data):
    """
    Analyzes input and output grids to extract properties.
    """
    analysis = {}
    for i, example in enumerate(task_data['train']):
        input_props = get_grid_properties(example['input'])
        output_props = get_grid_properties(example['output'])
        analysis[f'example_{i+1}'] = {
          'input': input_props,
          'output': output_props,
          'same_dims': (input_props['height'] == output_props['height']) and (input_props['width'] == output_props['width']),
        }
    return analysis

task_data = {
  "train": [
    {
      "input": [[0, 0, 8, 0, 0], [0, 8, 0, 8, 0], [0, 8, 8, 8, 0], [0, 8, 0, 8, 0], [0, 0, 8, 0, 0]],
      "output": [[0, 0, 8, 0, 0], [0, 8, 0, 8, 0], [0, 8, 8, 8, 0], [0, 8, 0, 8, 0], [0, 0, 8, 0, 0]]
    }
  ]
}

analysis = analyze_examples(task_data)
print(analysis)
