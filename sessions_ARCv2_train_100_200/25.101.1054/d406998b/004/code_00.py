# Code to calculate metrics for the simple SW+SE rule
import numpy as np

def transform_sw_se_rule(input_grid_list: list[list[int]]) -> list[list[int]]:
    input_grid = np.array(input_grid_list)
    height, width = input_grid.shape
    output_grid = np.copy(input_grid) # Start with input state

    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 5: # Only process gray pixels
                # Check SW
                sw_r, sw_c = r + 1, c - 1
                has_sw_gray = False
                if 0 <= sw_r < height and 0 <= sw_c < width and input_grid[sw_r, sw_c] == 5:
                    has_sw_gray = True

                # Check SE
                se_r, se_c = r + 1, c + 1
                has_se_gray = False
                if 0 <= se_r < height and 0 <= se_c < width and input_grid[se_r, se_c] == 5:
                    has_se_gray = True

                # Apply rule: If SW and SE are NOT both gray, change to green
                if not (has_sw_gray and has_se_gray):
                    output_grid[r, c] = 3
                # Otherwise, it stays 5 (as initially copied)

    return output_grid.tolist()

# Inputs and Expected Outputs
input1 = [[0,0,5,0,0,5,0,5,0,0,0,5,0],[5,0,0,0,5,0,5,0,0,5,0,0,5],[0,5,0,5,0,0,0,0,5,0,5,0,0]]
output1 = [[0,0,3,0,0,5,0,5,0,0,0,5,0],[3,0,0,0,3,0,3,0,0,5,0,0,3],[0,5,0,5,0,0,0,0,3,0,3,0,0]]
input2 = [[0,5,0,5,0,0,5,0,5,0,0,0],[5,0,0,0,5,0,0,5,0,0,5,0],[0,0,5,0,0,5,0,0,0,5,0,5]]
output2 = [[0,3,0,3,0,0,5,0,5,0,0,0],[5,0,0,0,5,0,0,3,0,0,5,0],[0,0,5,0,0,3,0,0,0,3,0,3]]
input3 = [[0,0,5,0,0,5,0,5,0,5,0,5,0,0],[5,0,0,0,5,0,0,0,5,0,5,0,0,5],[0,5,0,5,0,0,5,0,0,0,0,0,5,0]]
output3 = [[0,0,5,0,0,3,0,3,0,3,0,3,0,0],[5,0,0,0,5,0,0,0,5,0,5,0,0,3],[0,3,0,3,0,0,5,0,0,0,0,0,5,0]]
input4 = [[5,0,5,0,0,5,0,0,0,5],[0,5,0,0,5,0,0,5,0,0],[0,0,0,5,0,0,5,0,5,0]]
output4 = [[5,0,5,0,0,3,0,0,0,3],[0,3,0,0,5,0,0,3,0,0],[0,0,0,3,0,0,5,0,5,0]]

inputs = [input1, input2, input3, input4]
outputs = [output1, output2, output3, output4]

print("Metrics for Simple SW+SE Rule:")

for i, (inp, expected_outp) in enumerate(zip(inputs, outputs)):
    print(f"\n--- Example {i+1} ---")
    transformed_outp = transform_sw_se_rule(inp)
    inp_np = np.array(inp)
    expected_outp_np = np.array(expected_outp)
    transformed_outp_np = np.array(transformed_outp)

    correct_pixels = np.sum(transformed_outp_np == expected_outp_np)
    total_pixels = expected_outp_np.size
    accuracy = correct_pixels / total_pixels

    errors = {"should_be_5_is_3": 0, "should_be_3_is_5": 0}
    gray_pixels_input_indices = np.argwhere(inp_np == 5)

    for r, c in gray_pixels_input_indices:
        expected_val = expected_outp_np[r, c]
        transformed_val = transformed_outp_np[r, c]
        if expected_val != transformed_val:
            if expected_val == 5:
                errors["should_be_5_is_3"] += 1
            else: # expected_val == 3
                errors["should_be_3_is_5"] += 1

    print(f"  Accuracy: {accuracy:.2f}")
    print(f"  Total Errors: {total_pixels - correct_pixels}")
    print(f"    Errors (Should Stay 5, Changed to 3): {errors['should_be_5_is_3']}")
    print(f"    Errors (Should Change 3, Stayed 5): {errors['should_be_3_is_5']}") # This should be 0 for this specific rule
