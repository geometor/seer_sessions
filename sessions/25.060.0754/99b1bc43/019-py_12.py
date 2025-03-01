def analyze_example(example_index, input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    
    input_height, input_width = input_array.shape
    output_height, output_width = output_array.shape

    print(f"Example {example_index}:")
    print(f"  Input Dimensions: {input_width}x{input_height}")
    print(f"  Output Dimensions: {output_width}x{output_height}")
    
    colors_present = np.unique(input_array)
    print(f"  Colors Present in Input: {colors_present}")
    
    
    blue_red_yellow_positions = []
    for i in range(input_height):
        for j in range(input_width):
            if input_array[i, j] in [1, 2, 4]:
                blue_red_yellow_positions.append((i, j))
                
    print(f"  Positions of Blue(1), Red(2), Yellow(4) in input: {blue_red_yellow_positions}")

    output_colors = np.unique(output_array)
    print(f"  Colors present in Output: {output_colors}")

    mismatches = 0
    for row in range(min(4, input_height)):
       for col in range(min(4, input_width)):
           if (input_array[row][col] in (1,2,4)) != (output_array[row][col] == 3) :
               mismatches+=1
    print(f" Mismatches in first 4x4: {mismatches}")
    print("---")

for i in range(len(task["train"])): #conceptually task is a list of dictionaries with input/output pairs
  analyze_example(i+1, task["train"][i]["input"], task["train"][i]["output"])