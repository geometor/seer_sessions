import numpy as np

def calculate_metrics(grid):
    """Calculates object counts and other metrics for a given grid."""
    metrics = {}
    unique_colors = np.unique(grid)
    metrics['colors'] = unique_colors.tolist()
    metrics['color_counts'] = [np.sum(grid == color) for color in unique_colors]
    metrics['height'] = grid.shape[0]
    metrics['width'] = grid.shape[1]

    # basic object detection - contiguous regions of same color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r,c]:
                color = grid[r,c]
                obj_coords = []
                queue = [(r,c)]
                while queue:
                    qr, qc = queue.pop(0)
                    if (qr, qc) not in obj_coords: #prevent duplicates
                        obj_coords.append((qr, qc))
                    visited[qr, qc] = True
                    #check neighbors - must use same logic as get_neighbors
                    neighbors = [(qr-1, qc), (qr+1, qc), (qr, qc-1), (qr, qc+1)]
                    for nr, nc in neighbors:
                        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and not visited[nr, nc] and grid[nr, nc] == color:
                            queue.append((nr, nc))
                objects.append({'color': int(color), 'pixels': obj_coords})

    metrics['objects'] = objects
    metrics['object_count'] = len(objects)

    return metrics
def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate Gray pixels into 2x2 blocks
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 5:
                output_grid[row*2, col*2] = 5
                output_grid[row*2+1, col*2] = 5
                output_grid[row*2, col*2+1] = 5
                output_grid[row*2+1, col*2+1] = 5

    # Fill Azure and White pattern on even rows
    for row in range(0, output_height, 2):  # Iterate through even rows only
        for col in range(output_width):
            if output_grid[row, col] == 0: # Check if the cell is not occupied by gray
                if col % 2 == 0:
                    output_grid[row, col] = 8  # Even column: azure
                else:
                    output_grid[row, col] = 0  # Odd column: white

    return output_grid

def compare_outputs(expected_output, generated_output):
    """Compares the expected and generated outputs."""
    return np.array_equal(expected_output, generated_output)
#The current task ID
task_id = "63613498"
# Load the data for the task (replace with actual data loading)
import json
with open(f'./data/training/{task_id}.json', 'r') as f:
    task_data = json.load(f)

# Analyze each example
for i, example in enumerate(task_data['train']):
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    generated_output_grid = transform(input_grid)
    match = compare_outputs(expected_output_grid, generated_output)

    input_metrics = calculate_metrics(input_grid)
    expected_output_metrics = calculate_metrics(expected_output_grid)
    generated_output_metrics = calculate_metrics(generated_output_grid)


    print(f"Example {i+1}:")
    print(f"  Input Metrics: {input_metrics}")
    print(f"  Expected Output Metrics: {expected_output_metrics}")
    print(f"  Generated Output Metrics: {generated_output_metrics}")
    print(f"  Match: {match}")
    print("-" * 20)
