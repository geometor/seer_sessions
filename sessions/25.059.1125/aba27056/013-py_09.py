import numpy as np
from PIL import Image

def analyze_grid(grid, grid_name):
    """Analyzes a single grid and returns relevant metrics."""
    
    non_white_pixels = np.where(grid != 0)
    num_non_white_pixels = len(non_white_pixels[0])
    
    # Determine bounding box
    if num_non_white_pixels > 0:
        min_row, max_row = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
        min_col, max_col = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])
        bounding_box_area = (max_row - min_row + 1) * (max_col - min_col + 1)
    else:
        min_row, max_row, min_col, max_col = 0, 0, 0, 0
        bounding_box_area = 0

    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}

    metrics = {
        f"{grid_name}_height": grid.shape[0],
        f"{grid_name}_width": grid.shape[1],
        f"{grid_name}_num_non_white_pixels": num_non_white_pixels,
        f"{grid_name}_bounding_box_area": bounding_box_area,
        f"{grid_name}_min_row": min_row,
        f"{grid_name}_max_row": max_row,
        f"{grid_name}_min_col": min_col,
        f"{grid_name}_max_col": max_col,
        f"{grid_name}_unique_colors": unique_colors.tolist(),
        f"{grid_name}_color_counts": color_counts,
    }
    return metrics

def analyze_example(example_num):

    input_grid = np.array(Image.open(f'input_{example_num}.png').convert('L')) / 28
    output_grid = np.array(Image.open(f'output_{example_num}.png').convert('L')) / 28
    result_grid = np.array(Image.open(f'result_{example_num}.png').convert('L')) / 28

    input_metrics = analyze_grid(input_grid, "input")
    output_metrics = analyze_grid(output_grid, "output")
    result_metrics = analyze_grid(result_grid, "result")
    
    all_metrics = {**input_metrics, **output_metrics, **result_metrics}
    return all_metrics

# Analyze all examples
all_example_metrics = {}
for i in range(3):
    all_example_metrics[i] = analyze_example(i)

# Print results for review
for example_num, metrics in all_example_metrics.items():
    print(f"Example {example_num}:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")