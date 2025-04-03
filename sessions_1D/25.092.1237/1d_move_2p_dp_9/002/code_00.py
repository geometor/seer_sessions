# Simulate finding logic for example 1
input_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 6, 0, 0, 0]
expected_output_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 0, 0, 0]
main_color_1=4; main_start_1=9; main_length_1=10; marker_index_1=21
new_main_start_1 = main_start_1 + 2 # = 11
new_marker_index_1 = marker_index_1 # = 21 (Stays put)
# Generated Output matches Expected Output 1: True

# Simulate finding logic for example 2
input_2 = [0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 6, 0]
expected_output_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 0]
main_color_2=7; main_start_2=7; main_length_2=14; marker_index_2=23
new_main_start_2 = main_start_2 + 2 # = 9
new_marker_index_2 = marker_index_2 # = 23 (Stays put)
# Generated Output matches Expected Output 2: True

# Simulate finding logic for example 3
input_3 = [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
expected_output_3 = [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
main_color_3=5; main_start_3=3; main_length_3=7; marker_index_3=12
new_main_start_3 = main_start_3 + 2 # = 5
new_marker_index_3 = marker_index_3 # = 12 (Stays put)
# Generated Output matches Expected Output 3: True