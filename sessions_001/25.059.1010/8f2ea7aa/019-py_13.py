import numpy as np

# Example Data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 6, 6, 0, 0, 0],
                           [0, 6, 6, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 6],
                           [0, 0, 0, 0, 6, 6]]),
        "output": np.array([[6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6]]),
    },
   {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 6, 6, 0],
                           [0, 0, 0, 0, 0, 0, 6, 6, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 6, 6, 0],
                            [0, 0, 0, 0, 0, 0, 6, 6, 0]]),
    },
   {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 6, 6, 0, 0, 0, 0, 0],
                           [0, 6, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6]]),
    },    
  {
        "input": np.array([[6, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 6],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 6, 6, 0, 0, 0],
                           [0, 0, 6, 6, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6]]),
    }

]

def analyze_example(example):
    input_grid = example['input']
    output_grid = example['output']
    
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    # Determine if output contains all 6s
    all_sixes = np.all(output_grid == 6)
    
    # Execute the transform
    predicted_output = transform(input_grid.copy())

    correct = np.array_equal(predicted_output, output_grid)


    print(f"  Input Dimensions: {input_rows}x{input_cols}")
    print(f"  Output Dimensions: {output_rows}x{output_cols}")
    print(f"  Output is all sixes: {all_sixes}")
    print(f"  Prediction correct: {correct}")
    print(f"  Input:\n{input_grid}\nOutput:\n{output_grid}\nPredicted:\n{predicted_output}")

    return {
        "input_rows": input_rows,
        "input_cols": input_cols,
        "output_rows": output_rows,
        "output_cols": output_cols,
        "all_sixes": all_sixes
    }

results = []
for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    results.append(analyze_example(example))
