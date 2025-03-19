import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    predicted_array = np.array(predicted_output_grid)

    input_dims = input_array.shape
    output_dims = output_array.shape
    predicted_dims = predicted_array.shape

    input_colors = np.unique(input_array).tolist()
    output_colors = np.unique(output_array).tolist()
    predicted_colors = np.unique(predicted_array).tolist()

    correct = np.array_equal(output_array, predicted_array)

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Predicted Dimensions: {predicted_dims}")
    print(f"  Input Colors: {input_colors}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Predicted Output Colors: {predicted_colors}")
    print(f"  Correct Prediction: {correct}")

# input_output_pairs is a dictionary containing train and test examples
# load_task is defined and used in the main notebook
task = load_task("a85d4709", "train")

for i, example in enumerate(task['train']):
  predicted = transform(example['input'])
  print(f"Example {i+1}:")
  analyze_example(example['input'], example['output'], predicted)
