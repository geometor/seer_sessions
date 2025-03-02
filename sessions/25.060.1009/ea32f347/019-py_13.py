import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_grid):
    correct_pixels = np.sum(output_grid == predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels

    gray_blocks_input = len(find_contiguous_blocks(input_grid, 5))
    gray_blocks_output = len(find_contiguous_blocks(output_grid, 5))

    horizontal_input = 0
    vertical_input = 0
    for block in find_contiguous_blocks(input_grid, 5):
      if classify_orientation(block) == 'horizontal':
        horizontal_input += 1
      else:
        vertical_input += 1

    return {
        "accuracy": accuracy,
        "gray_blocks_input": gray_blocks_input,
        "gray_blocks_output": gray_blocks_output,
        "horizontal_gray_blocks_input": horizontal_input,
        "vertical_gray_blocks_input": vertical_input
    }
# need previous definitions of find_contiguous_blocks and classify_orientation

# dummy grids for testing during report generation (will be replaced with actual examples during notebook execution)
# example data will be loaded from files during code execution and metrics
# stored for each
example_metrics = []
# dummy data for testing
input_grid = output_grid = predicted_grid = np.array([[5]])
example_metrics.append(calculate_metrics(input_grid,output_grid,predicted_grid))
print(example_metrics)