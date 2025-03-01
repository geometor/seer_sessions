def show_grid(grid, title="Grid"):
    color_map = {
        0: (238, 238, 238),  # white
        1: (30, 147, 255),  # blue
        2: (220, 50, 40),  # red
        3: (79, 204, 48),  # green
        4: (230, 200, 0),  # yellow
        5: (85, 85, 85),  # gray
        6: (229, 58, 163),  # magenta
        7: (230, 120, 20),  # orange
        8: (135, 216, 241),  # azure
        9: (146, 18, 49),  # maroon
    }

    # Convert numerical values to color tuples
    colored_grid = np.array([[color_map[cell] for cell in row] for row in grid], dtype=np.uint8)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(colored_grid)

    # Customize the plot (optional)
    ax.set_title(title)
    ax.set_xticks([])  # Hide x-axis ticks
    ax.set_yticks([])  # Hide y-axis ticks

    plt.show()

def calculate_metrics(input_grid, predicted_output, expected_output):
    """Calculates metrics comparing predicted and expected outputs."""
    
    correct_pixels = np.sum(predicted_output == expected_output)
    total_pixels = predicted_output.size
    accuracy = correct_pixels / total_pixels
    
    changed_pixels_predicted = np.sum(predicted_output != input_grid)
    changed_pixels_expected = np.sum(expected_output != input_grid)
    
    grey_pixels_input = np.sum(input_grid == 5)
    blue_pixels_input = np.sum(input_grid == 1)
    
    metrics = {
        'accuracy': accuracy,
        'changed_pixels_predicted': changed_pixels_predicted,
        'changed_pixels_expected': changed_pixels_expected,
        'grey_pixels_input': grey_pixels_input,
        'blue_pixels_input': blue_pixels_input
    }
    
    return metrics

# Example usage (replace with actual grids)
for i, example in enumerate(task.train):
  input_grid = example["input"]
  expected_output = example["output"]
  predicted_output = transform(np.array(input_grid))
  metrics = calculate_metrics(np.array(input_grid), predicted_output, np.array(expected_output))
  print (f"Example: {i}")
  print (metrics)
  show_grid(np.array(input_grid), title="Input")
  show_grid(predicted_output, title = "Predicted")
  show_grid(np.array(expected_output), title="Expected")