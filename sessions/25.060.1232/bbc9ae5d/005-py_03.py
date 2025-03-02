import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)
    
    # Find blue region in input
    blue_region = find_blue_region(input_grid)
    if blue_region:
      input_blue_height = blue_region[2] - blue_region[0] + 1
      input_blue_width = blue_region[3] - blue_region[1] + 1
    else:
      input_blue_height = 0
      input_blue_width = 0
      
    # Find blue region in output
    blue_region_out = find_blue_region(output_grid)
    if blue_region_out:
      output_blue_height = blue_region_out[2] - blue_region_out[0] + 1
      output_blue_width = blue_region_out[3] - blue_region_out[1] + 1
    else:
      output_blue_height = 0
      output_blue_width = 0

    # Find blue region in prediction
    blue_region_pred = find_blue_region(predicted_output)
    if blue_region_pred:
        predicted_blue_height = blue_region_pred[2] - blue_region_pred[0] + 1
        predicted_blue_width = blue_region_pred[3] - blue_region_pred[1] + 1
    else:
        predicted_blue_height = 0
        predicted_blue_width = 0

    
    
    
    print(f"  Input Blue Region: Height={input_blue_height}, Width={input_blue_width}")
    print(f"  Output Blue Region: Height={output_blue_height}, Width={output_blue_width}")
    print(f"  Prediction Blue Region: Height={predicted_blue_height}, Width={predicted_blue_width}")
    print(f"  Correct Prediction: {np.array_equal(output_grid, predicted_output)}")

print("Example 1:")
analyze_example(task_json['train'][0]['input'], task_json['train'][0]['output'], transform(task_json['train'][0]['input']))
print("\nExample 2:")
analyze_example(task_json['train'][1]['input'], task_json['train'][1]['output'], transform(task_json['train'][1]['input']))
print("\nExample 3:")
analyze_example(task_json['train'][2]['input'], task_json['train'][2]['output'], transform(task_json['train'][2]['input']))
