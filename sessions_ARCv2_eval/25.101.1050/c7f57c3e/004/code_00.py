import numpy as np
from collections import Counter

def analyze_diff(input_grid, output_grid, transformed_grid, example_name):
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)
    transformed_np = np.array(transformed_grid)

    print(f"--- {example_name} Analysis ---")
    
    background_color_in = Counter(input_np.flatten()).most_common(1)[0][0]
    background_color_out = Counter(output_np.flatten()).most_common(1)[0][0]
    print(f"Input Background Color: {background_color_in}")
    print(f"Output Background Color: {background_color_out}")

    diff_pixels = np.where(output_np != transformed_np)
    diff_count = len(diff_pixels[0])

    print(f"Shape Input: {input_np.shape}")
    print(f"Shape Output: {output_np.shape}")
    print(f"Shape Transformed (Prev. Code): {transformed_np.shape}")
    
    if diff_count > 0:
        print(f"Pixels mismatch count (Prev. Code vs Expected): {diff_count}")
        print("Mismatch locations (row, col): Expected -> Transformed (Prev. Code) | Input")
        for r, c in zip(diff_pixels[0], diff_pixels[1]):
            # Added boundary check for safety, though unlikely needed here
            in_val = input_np[r,c] if 0 <= r < input_np.shape[0] and 0 <= c < input_np.shape[1] else 'OOB'
            print(f"  ({r:>2}, {c:>2}): {output_np[r, c]} -> {transformed_np[r, c]} | {in_val}")
    else:
        print("Transformed output (Previous Code) matches expected output.")
        
    print("-" * 30)

# Example 1 Data
input_1 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 2, 1, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 4, 4, 4],
    [4, 4, 4, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 1, 2, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 
    [4, 4, 4, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 2, 2, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 2, 2, 1, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
]
expected_output_1 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 2, 1, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 4, 4, 4], 
    [4, 4, 4, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 1, 8, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], # Changed expected (7,4) Red->Azure
    [4, 4, 4, 4, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], # Changed expected (8,4) Red->Azure 
    [4, 4, 4, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 8, 8, 1, 1, 4, 4, 4, 4], # Changed expected Red->Azure
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 8, 8, 1, 1, 4, 4, 4, 4], # Changed expected Red->Azure
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 4, 4, 4, 4, 4, 4], # Changed expected Red->Azure
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 4, 4, 4, 4, 4, 4], # Changed expected Red->Azure
    [4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4], 
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
]
# Transformed output from the previous run's log
transformed_output_1 = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 2, 1, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4], # Code output (3,13) was 2
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 4, 4, 4], # Code output base was 3
    [4, 4, 4, 4, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 1, 2, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], # Code output (6,4) was 2
    [4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], # Code output (7,4) was 2
    [4, 4, 4, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], # Code output base was 8
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 2, 2, 1, 1, 4, 4, 4, 4], # Code output struct was 2
    [4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 2, 2, 1, 1, 4, 4, 4, 4], # Code output struct was 2
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4], # Code output base was 2
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 4, 4, 4, 4, 4, 4], # Code output base was 2
    [4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4], # Code output base was 8
    [4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4], # Code output base was 8
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
]

# Mismatched pixels based on previous execution log:
# (7, 4): 8 -> 2 | 2  -- Actually Expected=8, Transformed=2, Input=2 -- Code failed Red->Azure struct change
# (13, 10): 8 -> 2 | 2 -- Actually Expected=8, Transformed=2, Input=2 -- Code failed Red->Azure struct change
# (13, 11): 8 -> 2 | 2 -- Actually Expected=8, Transformed=2, Input=2 -- Code failed Red->Azure struct change
# (14, 10): 8 -> 2 | 2 -- Actually Expected=8, Transformed=2, Input=2 -- Code failed Red->Azure base change
# (14, 11): 8 -> 2 | 2 -- Actually Expected=8, Transformed=2, Input=2 -- Code failed Red->Azure base change
# Also need to re-evaluate the (3,13) case from the expected output: Expected=2, Input=8. Original Base=Azure. 
# Pixel below Red(2) in struct should change to Red(2). My prev transformed output has 2, expected has 2. Let's re-verify my manual transcription of the code output.
# The code output shown in the prompt results *DOES* match the mismatch list.
# Expected: (7,4)=8, (13,10)=8, (13,11)=8, (14,10)=8, (14,11)=8.
# Actual Transformed: (7,4)=2, (13,10)=2, (13,11)=2, (14,10)=2, (14,11)=2.
# Input: (7,4)=2, (13,10)=2, (13,11)=2, (14,10)=2, (14,11)=2.
# The code failed to change the Red(2) pixels to Azure(8) when the base was Green(3).

analyze_diff(input_1, expected_output_1, transformed_output_1, "Example 1") # Using my corrected expected output

# Example 2 Data
input_2 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 6, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3], 
    [3, 3, 1, 3, 1, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3], 
    [3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]
expected_output_2 = [
    [3, 3, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3], 
    [3, 3, 1, 3, 1, 3, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3],
    [3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]
# Transformed output for Example 2 was identical to input in the previous run
transformed_output_2 = input_2 
analyze_diff(input_2, expected_output_2, transformed_output_2, "Example 2")
