import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find the green and blue pixels
    green_coords = find_pixel(input_grid, 3)
    blue_coords = find_pixel(input_grid, 1)

    if green_coords is None or blue_coords is None:
        return output_grid # Return empty grid if either color is not found

    # Horizontal Expansion and connection
    row_index = green_coords[0]
    mid_point = (green_coords[1] + blue_coords[1]) // 2
    
    # expand green to the left
    for c in range(green_coords[1], -1, -1):
        output_grid[row_index, c] = 3

    # expand green to the mid point
    for c in range(green_coords[1] + 1, mid_point):
        output_grid[row_index, c] = 3

    # expand blue to the right
    for c in range(blue_coords[1], len(output_grid[0])):
          output_grid[row_index, c] = 1
    # expand blue to the left up to the midpoint
    for c in range(blue_coords[1]-1, mid_point-1, -1):
      output_grid[row_index, c] = 1
    
    # vertical replication of the sequence
    for i in range(-2, 3):
        if row_index + i >= 0 and row_index + i < len(output_grid):
           output_grid[row_index + i, :] = output_grid[row_index,:]
           output_grid[row_index + i, green_coords[1]] = 3
           output_grid[row_index + i, blue_coords[1]] = 1

    return output_grid

def get_metrics(task):
    print(f"Task: {task['task_name']}")
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid.copy())  # Use a copy to avoid modifying the original
        
        #basic metrics
        green_coords = find_pixel(input_grid, 3)
        blue_coords = find_pixel(input_grid, 1)
        correct = np.array_equal(expected_output,predicted_output)

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'green_coords': green_coords,
            'blue_coords': blue_coords,
            'correct': correct,
            'predicted_output': predicted_output.tolist(),  # Convert to list for easier viewing
            'expected_output': expected_output.tolist()

        })
    for i,result in enumerate(results):
        print(f"  Example {i + 1}:")
        print(f"    Input Shape: {result['input_shape']}")
        print(f"    Output Shape: {result['output_shape']}")
        print(f"    Green Coords: {result['green_coords']}")
        print(f"    Blue Coords: {result['blue_coords']}")
        print(f"    Correct: {result['correct']}")
        if not result['correct']:
            print(f"    Predicted Output: \n{np.array(result['predicted_output'])}")
            print(f"    Expected Output:  \n{np.array(result['expected_output'])}")
    return results

# example use - using the file provided
import json
with open("6fa7a44f.json", 'r') as f:
    task = json.load(f)
results = get_metrics(task)