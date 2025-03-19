# Hypothetical Code for Metrics Gathering (for demonstration in dreamer phase)
import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and gathers metrics."""

    input_objects = find_objects(input_grid, 6) # as defined in the code
    output_objects = find_objects(output_grid, 3) # as defined in the code
    
    metrics = {
        "input_shapes": len(input_objects),
        "output_shapes": len(output_objects),
        "input_colors": list(np.unique(input_grid)),
        "output_colors": list(np.unique(output_grid)),
        "predicted_colors": list(np.unique(predicted_grid)),
        "output_equals_predicted": np.array_equal(output_grid, predicted_grid),
    }
    
    print(metrics)

# Example usage (hypothetical - dreamer can't run code directly)
for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)):
    predicted_grid = transform(input_grid.copy())
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid, predicted_grid)