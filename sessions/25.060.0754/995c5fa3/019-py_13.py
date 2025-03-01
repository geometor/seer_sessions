import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape
    predicted_rows, predicted_cols = predicted_output.shape

    all_white_rows_input = [i for i, row in enumerate(input_grid) if np.all(row == 0)]
    all_non_white_rows_input = [i for i, row in enumerate(input_grid) if np.all(row != 0)]
    mixed_rows_input = [i for i, row in enumerate(input_grid) if not np.all(row == 0) and not np.all(row != 0)]
    
    all_white_rows_output = [i for i, row in enumerate(output_grid) if np.all(row == 0)]
    all_non_white_rows_output = [i for i, row in enumerate(output_grid) if np.all(row != 0)]
    mixed_rows_output = [i for i, row in enumerate(output_grid) if not np.all(row == 0) and not np.all(row != 0)]


    print(f"  Input Grid Dimensions: {input_rows}x{input_cols}")
    print(f"  Output Grid Dimensions: {output_rows}x{output_cols}")
    print(f"  Predicted Grid Dimensions: {predicted_rows}x{predicted_cols}")
    print(f"  Input - All White Rows: {all_white_rows_input}")
    print(f"  Input - All Non-White Rows: {all_non_white_rows_input}")
    print(f"  Input - Mixed Rows: {mixed_rows_input}")
    print(f"  Output - All White Rows: {all_white_rows_output}")
    print(f"  Output - All Non-White Rows: {all_non_white_rows_output}")
    print(f"  Output - Mixed Rows: {mixed_rows_output}")

    correct = np.array_equal(output_grid, predicted_output)
    print(f"  Correct prediction: {correct}")

# input data is a list of tuples, [(input, output)]
def process_examples(io_examples, predicted_outputs):
    for i, (input_grid, output_grid) in enumerate(io_examples):
        print(f"Example {i+1}:")
        predicted_output = predicted_outputs[i]
        analyze_example(input_grid, output_grid, predicted_output)
        print("-" * 20)

# examples are from previous messages - packed as tuples
examples = [
    (np.array([[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]),
     np.array([[2, 2, 2],
               [2, 2, 2],
               [2, 2, 2]])),
    (np.array([[0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0],
               [1, 0, 0, 0, 0]]),
     np.array([[2, 2, 2],
               [1, 1, 1],
               [1, 1, 1]])),
    (np.array([[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0]]),
     np.array([[2, 2, 2],
               [2, 2, 2],
               [6, 6, 6]]))
]

# predicted outputs using previously defined transform
predicted_outputs = [transform(ex[0]) for ex in examples]
process_examples(examples, predicted_outputs)
