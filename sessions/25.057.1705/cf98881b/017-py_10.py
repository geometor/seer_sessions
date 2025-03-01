import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_output_shape = predicted_output.shape
    
    first_col_input = input_grid[:,0]
    non_yellow_input = first_col_input[first_col_input != 4]
    non_yellow_count_input = len(non_yellow_input)

    first_col_output = output_grid[:,0]
    non_yellow_output = first_col_output[first_col_output != 4]
    non_yellow_count_output = len(non_yellow_output)
    
    correct = np.array_equal(output_grid, predicted_output)

    print(f"Input shape: {input_shape}, Output shape: {output_shape}, Predicted Output shape: {predicted_output_shape}")
    print(f"Input First Column non-yellow count: {non_yellow_count_input}")
    print(f"Output First Column non-yellow count: {non_yellow_count_output}")
    print(f"Correct: {correct}")
    print("---")
    

# load the grids
task_data = [...] # paste the task data from the prompt here

for i, example in enumerate(task_data['train']):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  predicted_output = transform(input_grid)
  print(f"Example {i+1}:")
  analyze_example(input_grid, output_grid, predicted_output)
