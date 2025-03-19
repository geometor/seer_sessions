# hypothetical code_execution environment
examples = [
    {
        "input": np.array([[5, 5, 5], [5, 4, 5], [5, 5, 5]]),
        "output": np.array([[4, 4, 4], [4, 0, 4], [4, 4, 4]]),
    },
    {
        "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4]]),
    },
        {
        "input": np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    },
]

def check_example(example, transform_function):
  transformed = transform_function(example['input'])
  print(f"Transformed:\n{transformed}")
  print(f"Expected:\n{example['output']}")
  print(f"Correct: {np.array_equal(transformed, example['output'])}\n")

#this is a placeholder for the real function
def transform_function(input):
    output = np.copy(input)
    initial_yellow_pixels = []
    for i in range(input.shape[0]):
      for j in range(input.shape[1]):
        if input[i,j] == 4:
          initial_yellow_pixels.append((i,j))

    for i in range(input.shape[0]):
        for j in range(input.shape[1]):
            if output[i,j] == 5:
                output[i,j] = 4

    for (i,j) in initial_yellow_pixels:
      output[i,j] = 0
    return output
    
for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    check_example(example, transform_function)