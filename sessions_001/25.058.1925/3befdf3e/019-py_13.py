def check_solution(task):
    num_correct = 0
    for pair in task["train"]:
        input_grid = np.array(pair["input"])
        output_grid = np.array(pair["output"])
        predicted_output = transform(input_grid.copy())

        print(f"Example Pair: {pair}")

        inner_rect = find_rectangle(input_grid, 1)
        print(f"  Inner Rectangle (blue): {inner_rect}")

        outer_color = get_outer_rectangle_color(input_grid)
        print(f" Outer Color: {outer_color}")

        expanded_region = expand_perimeter(input_grid,inner_rect)
        print(f"  Expanded Region: {expanded_region}")

        if np.array_equal(predicted_output, output_grid):
            print("  Prediction: CORRECT")
            num_correct += 1
        else:
            print("  Prediction: INCORRECT")
            print(" predicted")
            print(predicted_output)
            print(" expected")
            print(output_grid)
    print(f"{num_correct} correct out of {len(task['train'])} attempts")

# Assuming 'task' variable is loaded with the ARC task data
check_solution(task)