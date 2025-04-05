import math

# Helper function to simulate the core logic
def apply_logic(input_list):
    output_list = list(input_list) # Work on a copy
    runs = []
    i = 0
    n = len(output_list)
    while i < n:
        if output_list[i] == 2:
            start_index = i
            j = i + 1
            while j < n and output_list[j] == 2:
                j += 1
            length = j - start_index
            runs.append((start_index, length))
            i = j
        else:
            i += 1

    for start_index, length in runs:
        num_to_change = length // 2
        if num_to_change > 0:
            change_start_index = start_index + length - num_to_change
            for k in range(change_start_index, start_index + length):
                output_list[k] = 8
    return output_list

# --- Training Example 1 ---
input_1 = [0, 2, 2, 0, 2, 2, 2, 0, 0, 0, 2, 2]
expected_1 = [0, 2, 8, 0, 2, 2, 8, 0, 0, 0, 2, 8]
predicted_1 = apply_logic(input_1)
match_1 = predicted_1 == expected_1

# --- Training Example 2 ---
input_2 = [0, 2, 2, 2, 2, 0, 2, 2, 0, 0, 2, 2]
expected_2 = [0, 2, 2, 8, 8, 0, 2, 8, 0, 0, 2, 8]
predicted_2 = apply_logic(input_2)
match_2 = predicted_2 == expected_2

# --- Training Example 3 ---
input_3 = [0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0]
expected_3 = [0, 2, 2, 8, 0, 2, 2, 2, 8, 8, 0, 0]
predicted_3 = apply_logic(input_3)
match_3 = predicted_3 == expected_3

# --- Training Example 4 ---
input_4 = [0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2]
expected_4 = [0, 2, 2, 8, 0, 2, 2, 2, 2, 8, 8, 8]
predicted_4 = apply_logic(input_4)
match_4 = predicted_4 == expected_4

# --- Training Example 5 ---
input_5 = [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2]
expected_5 = [0, 0, 0, 0, 0, 0, 2, 2, 8, 0, 2, 8]
predicted_5 = apply_logic(input_5)
match_5 = predicted_5 == expected_5

# --- Training Example 6 ---
input_6 = [0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0]
expected_6 = [0, 2, 8, 0, 2, 2, 8, 8, 0, 0, 0, 0]
predicted_6 = apply_logic(input_6)
match_6 = predicted_6 == expected_6

# --- Training Example 7 ---
input_7 = [0, 0, 0, 0, 2, 2, 0, 2, 2, 2, 2, 0]
expected_7 = [0, 0, 0, 0, 2, 8, 0, 2, 2, 8, 8, 0]
predicted_7 = apply_logic(input_7)
match_7 = predicted_7 == expected_7

print(f"Train 1 Match: {match_1}, Predicted: {predicted_1}")
print(f"Train 2 Match: {match_2}, Predicted: {predicted_2}")
print(f"Train 3 Match: {match_3}, Predicted: {predicted_3}")
print(f"Train 4 Match: {match_4}, Predicted: {predicted_4}")
print(f"Train 5 Match: {match_5}, Predicted: {predicted_5}")
print(f"Train 6 Match: {match_6}, Predicted: {predicted_6}")
print(f"Train 7 Match: {match_7}, Predicted: {predicted_7}")
