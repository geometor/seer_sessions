import numpy as np

def analyze_results(examples, transform_func):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        input_np = np.array(input_grid)
        expected_output_np = np.array(expected_output)
        predicted_output_np = transform_func(input_np)

        # Check if predicted output is equal to expected output.
        correct = np.array_equal(predicted_output_np, expected_output_np)

        # get the dimensions
        input_dims = input_np.shape
        
        if predicted_output_np.size != 0:
          predicted_dims = predicted_output_np.shape
        else:
          predicted_dims = (0, 0) # set dims to zero
          
        expected_dims = expected_output_np.shape

        results.append({
            "example": i + 1,
            "correct": correct,
            "input_dims": input_dims,
            "predicted_dims": predicted_dims,
            "expected_dims": expected_dims,
        })
    return results

# dummy examples - replace this with actual data
examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]],

        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 4, 3, 4, 2, 4, 4, 3, 2],
        [2, 4, 4, 3, 2, 3, 3, 4, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    ),
    (
        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 4, 3, 4, 2, 4, 4, 3, 2],
        [2, 4, 4, 3, 2, 3, 3, 4, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],        
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    ),
     (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 4, 3, 4, 2, 4, 4, 3, 2],
        [2, 4, 4, 3, 2, 3, 3, 4, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2, 2, 2, 2],
         [2, 4, 3, 4, 2, 4, 4, 3, 2],
         [2, 4, 4, 3, 2, 3, 3, 4, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    )
]

from previous_code import transform
analysis = analyze_results(examples, transform)

for result in analysis:
    print(f"Example {result['example']}:")
    print(f"  Correct: {result['correct']}")
    print(f"  Input Dims: {result['input_dims']}")
    print(f"  Predicted Dims: {result['predicted_dims']}")
    print(f"  Expected Dims: {result['expected_dims']}")
    print("-" * 20)