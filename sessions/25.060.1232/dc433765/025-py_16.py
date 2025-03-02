import numpy as np

def find_pixel(grid, color_value):
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:
       return (coords[0][0], coords[1][0])
    else: return None

def report(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        green_in = find_pixel(input_grid, 3)
        green_out = find_pixel(output_grid, 3)
        
        print(f"  Example {i+1}:")
        print(f"    Green Input : {green_in}")
        print(f"    Green Output: {green_out}")
        if green_in is not None:  # Only calculate if green pixel exists
            row_diff = green_out[0] - green_in[0]
            col_diff = green_out[1] - green_in[1]
            print(f"    Row Change  : {row_diff}")
            print(f"    Col Change  : {col_diff}")
        print(f"{'-' * 20}")

# Assuming `task` is a dictionary containing the 'train' examples.
# For demonstration, I'll create a dummy 'task' dictionary. Replace as needed.
# Create dummy data for demonstration
task = {
    'name': 'dummy_task',
    'train': [
      {'input': [[0, 0, 0], [0, 3, 0], [0, 0, 0]], 'output': [[0, 0, 0], [0, 0, 0], [0, 3, 0]]},
      {'input': [[0, 0, 3], [0, 0, 0], [0, 0, 0]], 'output': [[0, 0, 0], [0, 0, 3], [0, 0, 0]]},
      {'input': [[0, 0, 0, 0], [3, 0, 0, 0], [0, 0, 0, 0]], 'output': [[0, 0, 0, 0], [0, 0, 0, 0], [3, 0, 0, 0]]}
    ]
}
report(task)
