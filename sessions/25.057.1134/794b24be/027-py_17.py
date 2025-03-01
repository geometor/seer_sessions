# Conceptual code for gathering metrics (not executable in this turn)
# This block shows the KIND of analysis that informs the YAML and NL program.

def analyze_results(train_examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(train_examples):
        predicted_output = transform_function(input_grid.copy())  # Use a copy to avoid modifying the original
        
        # Compare the input, predicted output, and expected output.
        input_colored_pixel_coords = find_colored_pixel(input_grid)
        expected_colored_pixel_coords = find_colored_pixel(expected_output)

        input_color = input_grid[input_colored_pixel_coords] if input_colored_pixel_coords else 0
        expected_color = expected_output[expected_colored_pixel_coords] if expected_colored_pixel_coords else 0
        predicted_color = predicted_output[expected_colored_pixel_coords] if expected_colored_pixel_coords else 0

        correct_move =  np.array_equal(predicted_output,expected_output)

        results.append({
            "example_number": i,
            "input_color": input_color,
            "expected_color": expected_color,
            "predicted_color": predicted_color,
            "correct_move": correct_move
        })
    return results

# Example Usage (Conceptual - Requires the train_examples data)
# analysis_results = analyze_results(train_examples, transform)
# print(analysis_results)

#the result would look like this:
"""
[
    {
        "example_number": 0,
        "input_color": 6,
        "expected_color": 6,
        "predicted_color": 2,
        "correct_move": False
    },
    {
        "example_number": 1,
        "input_color": 2,
        "expected_color": 2,
        "predicted_color": 2,
        "correct_move": True
    },
      {
        "example_number": 2,
        "input_color": 3,
        "expected_color": 3,
        "predicted_color": 2,
        "correct_move": False
    },
]
"""