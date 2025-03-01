import numpy as np

def code_execution(input_grid, output_grid, predicted_output_grid):
    """
    Calculates and returns metrics comparing the expected output and
    the predicted output.
    """
    correct = np.array_equal(output_grid, predicted_output_grid)
    diff_grid = output_grid - predicted_output_grid
    match_value_count = 0
    for x,y in np.ndindex(diff_grid.shape):
        if output_grid[x,y] == predicted_output_grid[x,y]:
            match_value_count += 1
    metrics = {
        'correct': correct,
        'match_percent': match_value_count / output_grid.size * 100,
        'diff_grid': diff_grid.tolist(), # Convert to list for YAML
    }
    return metrics

# Example usage (assuming we have input_grid, output_grid, predicted_output)
# from the training set
task_data = [
    {
        "input": [[1, 0, 2], [0, 0, 0], [0, 0, 0]],
        "output": [[1, 5, 2], [0, 0, 0], [0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 6, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 6, 6, 8, 8, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    },
    {
      "input":  [[1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4]],
       "output": [[1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4]]
    }
]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the first row
    objects = find_objects(input_grid)
    
    #if there are two distinct objects
    if (len(objects) == 2):

        # Get the x-coordinates of the objects
        x1 = objects[0]['x']
        x2 = objects[1]['x']
        val1 = objects[0]['value']
        val2 = objects[1]['value']

        # Calculate the midpoint
        midpoint = cols // 2

        # Expand the first object to the right until the midpoint
        for x in range(x1, midpoint):
            output_grid[0][x] = val1

        # Expand the second object to the left until the midpoint
        for x in range(midpoint + 1, x2 + 1):
            output_grid[0][x] = val2

        # Insert the separator (5) at the midpoint
        output_grid[0][midpoint] = 5
    elif (len(objects) == 4):
        # Get the x-coordinates of the objects
        x1 = objects[0]['x']
        x2 = objects[1]['x']
        x3 = objects[2]['x']
        x4 = objects[3]['x']
        val1 = objects[0]['value']
        val2 = objects[1]['value']
        val3 = objects[2]['value']
        val4 = objects[3]['value']
        
        for x in range(x1, x2):
            output_grid[0][x] = val1
        for x in range(x2, x3):
            output_grid[0][x] = val2
        for x in range(x3, x4):
            output_grid[0][x] = val3
        for x in range(x4, cols):
            output_grid[0][x] = val4
        

    return output_grid

results = []
for i, item in enumerate(task_data):
  input_grid = np.array(item['input'])
  output_grid = np.array(item['output'])
  predicted_output_grid = transform(input_grid)
  example_results = code_execution(input_grid, output_grid, predicted_output_grid)
  results.append(example_results)
  print(f"Example {i+1}: {example_results['correct']} {example_results['match_percent']:.2f}%")
  print(f"Diff grid:\n{example_results['diff_grid']}")
