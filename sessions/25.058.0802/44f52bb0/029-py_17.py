import numpy as np

def grid_properties(grid):
    """Returns properties of a grid: dimensions, unique colors, and color counts."""
    grid_np = np.array(grid)
    unique_colors = np.unique(grid_np)
    color_counts = {color: np.sum(grid_np == color) for color in unique_colors}
    return {
        "dimensions": grid_np.shape,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

# Example usage (assuming train_in and train_out contain the example data)

examples_data = []

for i in range(len(train_in)):
    input_props = grid_properties(train_in[i])
    output_props = grid_properties(train_out[i])
    predicted_output = transform(train_in[i])
    prediction_props = grid_properties(predicted_output)
    examples_data.append({
        "example_index": i,
        "input_properties": input_props,
        "expected_output_properties": output_props,
        "predicted_output_properties": prediction_props
    })

for example in examples_data:
  print(example)