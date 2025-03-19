import numpy as np

def count_neighbors(grid, row, col):
    """Counts neighbors with the same color, including diagonals."""
    rows, cols = grid.shape
    target_color = grid[row, col]
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and grid[i, j] == target_color:
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid by removing pixels that have fewer than two neighbors of the same color.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid.
    for row in range(rows):
        for col in range(cols):
            # Count neighbors of the same color, including diagonals.
            neighbor_count = count_neighbors(input_grid, row, col)
            # If fewer than two neighbors, change to white (0).
            if neighbor_count < 2:
                output_grid[row, col] = 0

    return output_grid

def analyze_results(task):
    """Analyzes the results of applying the transform function to the task examples."""
    reports = {}
    for example_index, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)

        diff_grid = (predicted_output_grid != expected_output_grid).astype(int)
        incorrect_pixels = np.where(diff_grid != 0)
        incorrect_predicted_values = predicted_output_grid[incorrect_pixels]
        incorrect_expected_values = expected_output_grid[incorrect_pixels]

        report = {
            'diff_grid': diff_grid.tolist(),
            'incorrect_pixels': list(zip(incorrect_pixels[0].tolist(), incorrect_pixels[1].tolist())),
            'incorrect_predicted_values': incorrect_predicted_values.tolist(),
            'incorrect_expected_values': incorrect_expected_values.tolist(),
        }
        
        # add input bounding box and pixel counts
        objects = {}
        rows, cols = input_grid.shape
        for row in range(rows):
            for col in range(cols):
                color = input_grid[row,col]
                if color != 0:
                    if color not in objects:
                        objects[color] = {
                            'min_row': row,
                            'max_row': row,
                            'min_col': col,
                            'max_col': col,
                            'count': 0
                        }
                    else:
                        objects[color]['min_row'] = min(objects[color]['min_row'], row)
                        objects[color]['max_row'] = max(objects[color]['max_row'], row)
                        objects[color]['min_col'] = min(objects[color]['min_col'], col)
                        objects[color]['max_col'] = max(objects[color]['max_col'], col)
                    objects[color]['count'] += 1
        for obj_data in objects.values():
          obj_data['height'] = obj_data['max_row'] - obj_data['min_row'] + 1
          obj_data['width'] = obj_data['max_col'] - obj_data['min_col'] + 1
        report['input_objects'] = objects

        reports[f'example_{example_index}'] = report
    return reports
# dummy task data for demonstration and running in notebook
task = {
  'train': [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 0, 0, 0, 8, 0, 0], [0, 8, 0, 8, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 0, 0, 0, 8, 0, 0], [0, 8, 0, 8, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 6, 0, 0, 0, 0, 0, 0, 0, 6]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}
  ]
}
reports = analyze_results(task)
for example, report in reports.items():
  print(f'{example=}')
  print(f"{report['input_objects']=}")
  print(f"{report['diff_grid']=}")
  print(f"{report['incorrect_pixels']=}")
  print(f"{report['incorrect_predicted_values']=}")
  print(f"{report['incorrect_expected_values']=}")