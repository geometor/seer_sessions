import numpy as np

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    stripe_col = -1
    for j in range(input_grid.shape[1]):
        if np.any(input_grid[:, j] == 1):
            stripe_col = j
            break

    input_height, input_width = input_grid.shape
    expected_height, expected_width = expected_output_grid.shape
    predicted_height, predicted_width = predicted_output_grid.shape

    correct_pixels = np.sum(predicted_output_grid == expected_output_grid)
    total_pixels = predicted_output_grid.size
    accuracy = (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0.0
    print(f"    Stripe Column: {stripe_col}")
    print(f"    Input Dimensions: {input_height}x{input_width}")
    print(f"    Expected Output Dimensions: {expected_height}x{expected_width}")
    print(f"    Predicted Output Dimensions: {predicted_height}x{predicted_width}")
    print(f"    Accuracy: {accuracy:.2f}%")

def show_grid(grid, label):
    print(f'    {label}')
    print(grid)

# Example Usage (assuming 'transform' function and example data are available)
examples = [
    (train_input_0, train_output_0, transform(train_input_0)),
    (train_input_1, train_output_1, transform(train_input_1)),
    (train_input_2, train_output_2, transform(train_input_2)),
    (train_input_3, train_output_3, transform(train_input_3)),
    (train_input_4, train_output_4, transform(train_input_4))
]

for i, (inp, exp, pred) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(inp, exp, pred)
    show_grid(inp, "Input")
    show_grid(exp, "Expected")
    show_grid(pred, "Predicted")

