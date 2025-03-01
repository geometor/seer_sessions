from utils import get_task_data, show_grid

def describe_grid(grid, grid_name):
    """
    Provides a basic description of a grid: dimensions and unique colors.
    """
    dimensions = grid.shape
    unique_colors = np.unique(grid)
    color_names = [
        "white", "blue", "red", "green", "yellow", "gray",
        "magenta", "orange", "azure", "maroon"
    ]
    color_descriptions = [color_names[c] for c in unique_colors]

    print(f"{grid_name}:")
    print(f"  Dimensions: {dimensions}")
    print(f"  Unique Colors: {color_descriptions}")

task = '6f8cd795'
train_data, test_data = get_task_data(task)

for example_num, (input_grid, output_grid) in enumerate(train_data):
    print(f"--- Example {example_num} ---")
    show_grid(input_grid, "Input")
    show_grid(output_grid, "Output")
    describe_grid(input_grid, "Input Grid")
    describe_grid(output_grid, "Output Grid")

    # make predictions with current transform function and show results
    output_prediction = transform(input_grid)
    show_grid(output_prediction, "Predicted Output")
    describe_grid(output_prediction, f"Predicted Output Grid Example: {example_num}")
    if np.array_equal(output_grid, output_prediction):
        print("Prediction: Correct")
    else:
        print("Prediction: Incorrect")
