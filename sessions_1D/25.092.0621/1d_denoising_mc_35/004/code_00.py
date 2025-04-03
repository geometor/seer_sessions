import numpy as np
from collections import Counter
import json

def analyze_example(input_str, output_str):
    # Helper to parse the string representation into a numpy array
    input_grid_list = [int(x) for x in input_str.split()]
    output_grid_list = [int(x) for x in output_str.split()]

    # Convert to numpy array - treat as 1 row
    input_grid = np.array([input_grid_list])
    output_grid = np.array([output_grid_list])

    # Convert shapes (tuples) to lists for JSON serialization
    input_shape = list(input_grid.shape)
    output_shape = list(output_grid.shape)

    background_color = 0
    non_background_indices_input = np.argwhere(input_grid != background_color)

    # Initialize with Python types
    dominant_color_input = None
    object_pixels_input_list = []
    object_coords_input_list = []

    if non_background_indices_input.size > 0:
        min_col = non_background_indices_input[:, 1].min()
        max_col = non_background_indices_input[:, 1].max()
        # Ensure coordinates are lists of Python ints
        object_coords_input_list = non_background_indices_input.tolist()
        # Extract the relevant segment from the original list for correct pixel values
        object_pixels_input = input_grid[0, min_col:max_col+1]
        object_pixels_input_list = [int(p) for p in object_pixels_input] # Convert numpy ints to Python ints

        if object_pixels_input.size > 0:
            color_counts = Counter(object_pixels_input)
            # Convert numpy int to Python int
            dominant_color_input = int(color_counts.most_common(1)[0][0])
        # else: dominant_color_input remains None

    # Analyze output object
    non_background_indices_output = np.argwhere(output_grid != background_color)
    output_object_color = None
    output_object_is_uniform = None # Use None for undefined cases

    if non_background_indices_output.size > 0:
         min_col_out = non_background_indices_output[:, 1].min()
         max_col_out = non_background_indices_output[:, 1].max()
         object_pixels_output = output_grid[0, min_col_out:max_col_out+1]
         if object_pixels_output.size > 0:
             # Convert potential numpy int/bool to Python types
             output_object_color = int(object_pixels_output[0])
             output_object_is_uniform = bool(len(np.unique(object_pixels_output)) <= 1)
         # else: output_object_color/uniformity remain None

    # Calculate dominant_matches_output using Python types
    dominant_matches_output = (dominant_color_input == output_object_color) if (dominant_color_input is not None and output_object_color is not None) else None


    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "non_background_indices_input_count": len(non_background_indices_input),
        "input_object_coords": object_coords_input_list,
        "input_object_pixels": object_pixels_input_list,
        "dominant_color_input": dominant_color_input,
        "output_object_color": output_object_color,
        "output_object_is_uniform": output_object_is_uniform,
        "dominant_matches_output": dominant_matches_output
    }

# Example Data
examples = [
    {
        "input": "0 0 0 0 8 8 1 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 7 8 8 8 8 0 0 0",
        "output": "0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0"
    },
    {
        "input": "0 0 0 0 4 4 4 4 4 7 4 4 4 4 4 6 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0",
        "output": "0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0"
    },
    {
        "input": "0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 3 7 7 7 4 7 7 0 0 0 0 0",
        "output": "0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0"
    }
]

results = []
for i, ex in enumerate(examples):
    # print(f"Analyzing Example {i+1}") # Keep console clean for final output
    results.append(analyze_example(ex["input"], ex["output"]))

# Print results cleanly
print(json.dumps(results, indent=2))