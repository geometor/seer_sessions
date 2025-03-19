import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Find the azure pixel in the input
        azure_pixels_input = np.where(input_grid == 8)
        num_azure_pixels_input = len(azure_pixels_input[0])
        start_pixel = find_start_pixel(input_grid)

        
        input_azure_coords = list(zip(azure_pixels_input[0], azure_pixels_input[1]))
        
        # Find the azure pixel in the output
        azure_pixels_output = np.where(output_grid == 8)
        num_azure_pixels_output = len(azure_pixels_output[0])
        output_azure_coords = list(zip(azure_pixels_output[0], azure_pixels_output[1]))


        
        results.append({
            'input_azure_count': num_azure_pixels_input,
            'input_azure_coords': input_azure_coords,
            'output_azure_count': num_azure_pixels_output,
            'output_azure_coords': output_azure_coords,
            'start_pixel': start_pixel,
        })
    return results

# Assuming 'task' is defined elsewhere and contains the task data.
# The following line is for demonstration purposes. Replace it with the actual task data.
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5, 0, 0, 0, 5, 0, 0, 0, 5], [0, 5, 0, 0, 5, 0, 0, 5, 0], [0, 0, 5, 0, 8, 0, 5, 0, 0], [0, 5, 0, 0, 5, 0, 0, 5, 0], [5, 0, 0, 0, 5, 0, 0, 0, 5]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 0, 0, 0, 0], [0, 5, 0, 5, 0, 5, 0, 0, 0], [5, 5, 5, 8, 5, 5, 5, 5, 5], [0, 5, 0, 5, 0, 5, 0, 0, 0], [0, 0, 5, 5, 5, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 8, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0]],
        },
    ]
}

analysis = analyze_results(task)
print(analysis)

def find_start_pixel(grid, color=8):
    # Find the coordinates of the pixel with the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return row and column
    return None