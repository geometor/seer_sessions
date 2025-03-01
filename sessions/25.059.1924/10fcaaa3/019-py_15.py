def analyze_example(input_grid, output_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    red_pixels_input = np.argwhere(input_grid == 2)
    red_pixels_output = np.argwhere(output_grid == 2)
    azure_pixels_output = np.argwhere(output_grid == 8)

    print(f"Input Dimensions: {input_height}x{input_width}")
    print(f"Output Dimensions: {output_height}x{output_width}")
    print(f"Red Pixels (Input):\n{red_pixels_input}")
    print(f"Red Pixels (Output):\n{red_pixels_output}")
    print(f"Azure Pixels (Output):\n{azure_pixels_output}")

# Example data - replace with actual data from the task
example1 = {
    "input": np.array([[0, 0, 0, 0],
                       [0, 2, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
    "output": np.array([[8, 0, 8, 0, 8, 0, 8, 0],
                        [0, 2, 0, 0, 0, 2, 0, 0],
                        [8, 0, 8, 0, 8, 0, 8, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [8, 0, 8, 0, 8, 0, 8, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [8, 0, 8, 0, 8, 0, 8, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]])
}
example2 = {
"input" : np.array([[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 2, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]]),
"output" :  np.array([[8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [8, 0, 8, 0, 8, 2, 8, 0, 8, 2, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
}

example3 = {
    "input":  np.array([[0, 0, 0],
                       [0, 2, 0],
                       [0, 0, 0]]),
    "output": np.array([[8, 0, 8, 0, 8, 0],
                        [0, 2, 0, 0, 0, 2],
                        [8, 0, 8, 0, 8, 0],
                        [0, 0, 0, 0, 0, 0],
                        [8, 0, 8, 0, 8, 0],
                        [0, 0, 0, 0, 0, 0]])
}

analyze_example(example1["input"], example1["output"])
analyze_example(example2["input"], example2["output"])
analyze_example(example3["input"], example3["output"])
