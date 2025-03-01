import numpy as np

def get_object_stats(grid, object_value):
    """Find the coords of an object and compute location stats"""
    coords = np.argwhere(grid == object_value)
    if len(coords) == 0:
        return {}
    
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    
    return {
        'coords': coords.tolist(),
        'min_row': min_row,
        'min_col': min_col,
        'max_row': max_row,
        'max_col': max_col,
        'width': width,
        'height': height,
    }

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyze an example and return observations, concentrate on magenta"""
    input_magenta_stats = get_object_stats(input_grid, 6)
    output_magenta_stats = get_object_stats(output_grid, 6)
    predicted_magenta_stats = get_object_stats(predicted_grid,6)
    
    input_azure_stats = get_object_stats(input_grid, 8)
    output_azure_stats = get_object_stats(output_grid, 8)
    predicted_azure_stats = get_object_stats(predicted_grid, 8)

    
    return {
        'input_magenta':input_magenta_stats,
        'output_magenta': output_magenta_stats,
        'predicted_magenta':predicted_magenta_stats,
        'input_azure': input_azure_stats,
        'output_azure':output_azure_stats,
        'predicted_azure':predicted_azure_stats,
        'match': np.array_equal(output_grid, predicted_grid)
        
    }

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # iterate input grid
    for row in range(input_height):
        for col in range(input_width):
            # magenta replication
            if input_grid[row, col] == 6:
                output_grid[row, col] = 6
                output_grid[row, col + (output_width // 2) ] = 6
    
    # azure fill rows
    for row in range(output_height):
      if 6 in output_grid[row]:
        output_grid[row,:] = [8 if x == 0 else x for x in output_grid[row,:] ]

    # azure fill between columns
    magenta_cols = [ c for c in range(output_width) if 6 in output_grid[:,c] ]
    if len(magenta_cols) > 1:
      for r in range(output_height):
        for c in range(min(magenta_cols), max(magenta_cols) + 1):
          if output_grid[r,c] == 0:
            output_grid[r,c] = 8

    return output_grid

# Example usage (assuming you have your task data loaded)
task_id = '3618c87e'
with open(f'{task_id}.json', 'r') as f:
    task = json.load(f)

train_results = []
for example in task['train']:
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_grid = transform(input_grid)
    analysis = analyze_example(input_grid, output_grid, predicted_grid)
    train_results.append(analysis)

print(json.dumps(train_results, indent=2))
