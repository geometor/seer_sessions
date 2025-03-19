import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    """Calculates metrics comparing the output and predicted output grids."""
    metrics = {}

    # Check if grids are the same shape
    if output_grid.shape != predicted_output_grid.shape:
        metrics['shape_match'] = False
        metrics['pixel_accuracy'] = 0.0
        metrics['error_count'] = np.sum(output_grid != predicted_output_grid)
        return metrics
    else:
        metrics['shape_match'] = True

    # Calculate pixel accuracy
    correct_pixels = np.sum(output_grid == predicted_output_grid)
    total_pixels = output_grid.size
    metrics['pixel_accuracy'] = (correct_pixels / total_pixels) if total_pixels > 0 else 0.0
    metrics['error_count'] = np.sum(output_grid != predicted_output_grid)

    return metrics
def print_grid(grid, title="Grid"):
  """Prints a grid with a title."""

  print(f"\n--- {title} ---")
  for row in grid:
    print("".join(str(cell) for cell in row))