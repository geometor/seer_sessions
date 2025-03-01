import numpy as np

def code_execution(input_grid, output_grid, predicted_output = None):
    """
    Executes the transformation function on the input and compares it to the expected output.
    """
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)
    
    if predicted_output is None:
        predicted_output_np = transform(input_np)
    else:
        predicted_output_np = np.array(predicted_output)

    if predicted_output_np is None:
      result = "Function returned None"
    else:
      comparison = np.array_equal(predicted_output_np, output_np)
      result = "Match" if comparison else "Mismatch"
    
    print(f"Input:\n{input_np}\n")
    print(f"Expected Output:\n{output_np}\n")
    print(f"Predicted Output:\n{predicted_output_np}\n")
    print(f"Result: {result}\n")
    print("-" * 20)

# Provided Example Data (from prompt history)
examples = [
    (
        [[8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 8],
         [8, 8, 8, 8, 8, 8, 8, 8, 0],
         [8, 8, 8, 8, 8, 8, 8, 8, 0],
         [8, 8, 8, 8, 8, 8, 8, 8, 0],
         [8, 8, 8, 8, 8, 8, 8, 8, 0],
         [8, 8, 8, 8, 8, 8, 8, 8, 0],
         [8, 8, 8, 8, 8, 8, 0, 0, 0],
         [8, 8, 8, 8, 8, 8, 0, 3, 3],
         [8, 8, 8, 8, 8, 8, 0, 3, 3]],

        [[3, 3, 3],
         [3, 3, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3]]
    ),
    (
        [[0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 8, 8, 8, 8, 8, 8, 8, 0],
         [0, 3, 3, 8, 8, 8, 8, 8, 0],
         [0, 3, 3, 8, 8, 8, 8, 8, 0]],

        [[3, 3, 3],
         [3, 3, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

        [[3, 3, 3],
         [3, 3, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3],
         [0, 0, 3]]
    ),
]

for input_grid, output_grid in examples:
  code_execution(input_grid, output_grid)
