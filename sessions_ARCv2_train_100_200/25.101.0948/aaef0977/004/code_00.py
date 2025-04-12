import numpy as np

# The Base Sequence derived from Example 1 (where v0=3, shift=0)
BASE_SEQ = np.array([3, 4, 0, 5, 2, 8, 9, 6, 1])

def calculate_output_new_rule(grid_shape, r0, c0, v0):
    """Calculates the output grid based on the hypothesized rule."""
    height, width = grid_shape
    output = np.zeros((height, width), dtype=int)
    # Calculate the shift based on v0
    shift = (6 * v0) % 9
    for r in range(height):
        for c in range(width):
            # Calculate Manhattan distance
            dist = abs(r - r0) + abs(c - c0)
            # Calculate the index into the base sequence
            index = (dist + shift) % 9
            # Assign the value from the base sequence
            output[r, c] = BASE_SEQ[index]
    return output

# --- Example 1 Verification ---
r0_1, c0_1, v0_1 = 0, 6, 3
expected_1 = np.array([
    [9, 8, 2, 5, 0, 4, 3, 4],
    [6, 9, 8, 2, 5, 0, 4, 0],
    [1, 6, 9, 8, 2, 5, 0, 5],
    [3, 1, 6, 9, 8, 2, 5, 2],
    [4, 3, 1, 6, 9, 8, 2, 8],
    [0, 4, 3, 1, 6, 9, 8, 9],
    [5, 0, 4, 3, 1, 6, 9, 6],
    [2, 5, 0, 4, 3, 1, 6, 1]
])
calculated_1 = calculate_output_new_rule(expected_1.shape, r0_1, c0_1, v0_1)
match_1 = np.array_equal(expected_1, calculated_1)
mismatch_count_1 = np.count_nonzero(expected_1 != calculated_1)

print("--- Example 1 Verification ---")
print(f"Unique Pixel: ({r0_1}, {c0_1}), Value: {v0_1}")
print(f"Rule: Output = BaseSeq[(d + (6*{v0_1})%9) % 9] = BaseSeq[(d + 0) % 9]")
print(f"Match: {match_1}")
print(f"Mismatch Count: {mismatch_count_1} / {expected_1.size}")
if not match_1:
    print("Expected Output:")
    print(expected_1)
    print("Calculated Output:")
    print(calculated_1)


# --- Example 2 Verification ---
r0_2, c0_2, v0_2 = 5, 2, 5
expected_2 = np.array([
    [4, 3, 1, 3, 4, 0, 5, 2],
    [3, 1, 6, 1, 3, 4, 0, 5],
    [1, 6, 9, 6, 1, 3, 4, 0],
    [6, 9, 8, 9, 6, 1, 3, 4],
    [9, 8, 2, 8, 9, 6, 1, 3],
    [8, 2, 5, 2, 8, 9, 6, 1],
    [9, 8, 2, 8, 9, 6, 1, 3],
    [6, 9, 8, 9, 6, 1, 3, 4]
])
calculated_2 = calculate_output_new_rule(expected_2.shape, r0_2, c0_2, v0_2)
match_2 = np.array_equal(expected_2, calculated_2)
mismatch_count_2 = np.count_nonzero(expected_2 != calculated_2)

print("\n--- Example 2 Verification ---")
print(f"Unique Pixel: ({r0_2}, {c0_2}), Value: {v0_2}")
print(f"Rule: Output = BaseSeq[(d + (6*{v0_2})%9) % 9] = BaseSeq[(d + 3) % 9]")
print(f"Match: {match_2}")
print(f"Mismatch Count: {mismatch_count_2} / {expected_2.size}")
if not match_2:
    print("Expected Output:")
    print(expected_2)
    print("Calculated Output:")
    print(calculated_2)