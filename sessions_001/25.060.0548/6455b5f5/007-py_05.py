import numpy as np

def analyze_example(input_grid, output_grid):
    metrics = {}
    metrics['input_shape'] = input_grid.shape
    metrics['output_shape'] = output_grid.shape

    def get_pixel_coords(grid, color):
        coords = np.where(grid == color)
        return list(zip(coords[0], coords[1]))

    metrics['input_red_pixels'] = get_pixel_coords(input_grid, 2)
    metrics['output_red_pixels'] = get_pixel_coords(output_grid, 2)
    metrics['input_azure_pixels'] = get_pixel_coords(input_grid, 8)
    metrics['output_azure_pixels'] = get_pixel_coords(output_grid, 8)
    
    if len(metrics['input_red_pixels']) >0:
      metrics['input_red_min_y'] = min(metrics['input_red_pixels'])[0]
      metrics['input_red_max_y'] = max(metrics['input_red_pixels'])[0]
    else:
      metrics['input_red_min_y'] = None
      metrics['input_red_max_y'] = None

    if len(metrics['output_azure_pixels'])>0:
      metrics['output_azure_min_y'] = min(metrics['output_azure_pixels'])[0]
      metrics['output_azure_max_y'] = max(metrics['output_azure_pixels'])[0]
    else:
      metrics['output_azure_min_y'] = None
      metrics['output_azure_max_y'] = None

    return metrics

# Assuming 'task' is defined elsewhere and contains the training examples
task = {  # Replace with your actual task data structure
     'train': [
         {'input': np.array([[0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 0, 0]]), 'output': np.array([[1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 2, 8],
       [1, 1, 1, 1, 1, 1]])},
  {'input': np.array([[0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0]]), 'output': np.array([[1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 2, 8],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1]])},
  {'input': np.array([[0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 2, 0, 0],
       [0, 0, 0, 0, 0]]), 'output': np.array([[1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 2, 8, 1],
       [1, 1, 1, 1, 1]])},
  {'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 2, 8, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1]])},
    ],
    'test': [
        {'input': np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]), 'output': np.array([[1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 2, 8],
       [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1]])}
    ]
}

results = []
for example in task['train']:
    results.append(analyze_example(example['input'], example['output']))

for item in results:
    print(item)