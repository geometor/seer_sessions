import numpy as np
from skimage.measure import label, regionprops

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""

    # Find red pixels in input and output
    input_red_pixels = np.argwhere(input_grid == 2)
    output_red_pixels = np.argwhere(output_grid == 2)
    input_azure_pixels = np.argwhere(input_grid == 8)
    output_azure_pixels = np.argwhere(output_grid == 8)
    # Find connected regions of red pixels in the input
    labeled_input_red = label(input_grid == 2, connectivity=2)
    input_red_regions = regionprops(labeled_input_red)
    num_red_regions = len(input_red_regions)

    input_red_pixel_count = len(input_red_pixels) if len(input_red_pixels) >0 else 0
    output_red_pixel_count = len(output_red_pixels) if len(output_red_pixels) > 0 else 0
    input_azure_pixel_count = len(input_azure_pixels) if len(input_azure_pixels) > 0 else 0
    output_azure_pixel_count = len(output_azure_pixels) if len(output_azure_pixels) >0 else 0
    return {
        'input_red_pixels': input_red_pixel_count,
        'output_red_pixels': output_red_pixel_count,
        'input_red_regions': num_red_regions,
        'input_azure_pixels': input_azure_pixel_count,
        'output_azure_pixels': output_azure_pixel_count
    }

def analyze_all_examples(task):
    """Analyzes all examples in a task."""

    all_results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        results = analyze_example(input_grid, output_grid)
        all_results.append(results)
    return all_results

# Example Usage (replace with your actual task data):
# Assuming 'task' is a dictionary containing the 'train' examples
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 2, 2, 2, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 8, 8, 8, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 0], [0, 0, 2, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0], [0, 0, 8, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0], [0, 0, 2, 2, 2, 0], [0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2]], 'output': [[0, 0, 0, 0, 8, 0], [0, 0, 0, 8, 0, 0], [0, 0, 8, 8, 8, 0], [0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8]]}
    ]
}

results = analyze_all_examples(task)

for i, r in enumerate(results):
  print(f'example {i+1}:')
  print(r)