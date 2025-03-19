def analyze_example(input_grid, expected_output, transform_function):
    """Analyzes a single example and returns relevant metrics."""
    import numpy as np

    predicted_output = transform_function(input_grid)
    is_correct = np.array_equal(predicted_output, expected_output)
    maroon_coords_input = find_object(input_grid, 9)
    maroon_coords_output = find_object(predicted_output, 9) # use predicted

    return {
        "input_dims": input_grid.shape,
        "output_dims": expected_output.shape,
        "maroon_input": maroon_coords_input[0] if maroon_coords_input else None,
        "maroon_output": maroon_coords_output[0] if maroon_coords_output else None,
        "other_colors": [color for color in np.unique(input_grid) if color != 0 and color != 9],
        "correct": is_correct,
    }

# Hypothetical execution (replace with actual execution in a suitable environment)
examples = [
  # simplified representations for demonstration
    {"input": np.array([[1,0,0],[9,0,0],[0,0,0]]), "output": np.array([[1,0,0],[0,0,0],[9,0,0]])},
    {"input": np.array([[9,0,0],[0,0,0],[0,0,0]]), "output": np.array([[0,0,0],[9,0,0],[0,0,0]])},
    {"input": np.array([[0,0,9],[0,0,0],[0,0,0]]), "output": np.array([[0,0,0],[0,0,9],[0,0,0]])},
    {"input": np.array([[0,0,0],[0,0,0],[0,0,9]]), "output": np.array([[0,0,0],[0,0,0],[0,0,9]])},
]

results = [analyze_example(ex["input"], ex["output"], transform) for ex in examples]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Dims: {res['input_dims']}")
    print(f"  Output Dims: {res['output_dims']}")
    print(f"  Maroon Input: {res['maroon_input']}")
    print(f"  Maroon Output: {res['maroon_output']}")
    print(f"  Other Colors: {res['other_colors']}")
    print(f"  Correct: {res['correct']}")
    print("-" * 20)
