# John Byron Garin
# 2021-02658

def readFile():
    with open('hmm.in', 'r') as file:
        content = file.read().splitlines()
    number_of_strings = int(content[0])
    input_strings = content[1:1 + number_of_strings]
    possible_states = list(content[1 + number_of_strings].replace(" ", ""))
    possible_measurements = list(content[2 + number_of_strings].replace(" ", ""))
    probability_array = [float(value) for line in content[3 + number_of_strings:5 + number_of_strings] for value in line.split()]
    number_of_cases = int(content[5 + number_of_strings])

    # Initialize arrays to store the formatted strings and numbers
    formatted_array = []
    numbers_array = []
    original = []

    # Loop through each input case
    for case in content[6 + number_of_strings:]:
        original.append(case)
        tokens = case.split()
        formatted_array.append([tokens[0][0], tokens[2][0]])
        numbers_array.append(int(tokens[0][1:]))

    return original, number_of_strings, input_strings, possible_states, possible_measurements, probability_array, number_of_cases, formatted_array, numbers_array


def given_probabilities(possible_states, possible_measurements, probability_array):
    # sets the strings to be used later as dictionary keys
    first = possible_measurements[0] + "|" + possible_states[0]
    second = possible_measurements[1] + "|" + possible_states[0]
    third = possible_measurements[0] + "|" + possible_states[1]
    fourth = possible_measurements[1] + "|" + possible_states[1]

    first_value = probability_array[0]
    second_value = probability_array[1]
    third_value = probability_array[2]
    fourth_value = probability_array[3]

    given_probabilities = {
        first: first_value,
        second: second_value,
        third: third_value,
        fourth: fourth_value
    }

    first_measurement_probab_array = []
    second_measurement_probab_array = []

    return given_probabilities, first_measurement_probab_array, second_measurement_probab_array

def computed_probabilities(possible_states, string_sequence):
    # uses the possible states as dictionary keys
    computed_state_probab_dict = {
        possible_states[0]: [],
        possible_states[1]: []
    }

    # sets the strings to be used later as dictionary keys
    first = possible_states[0] + "|" + possible_states[0]
    second = possible_states[1] + "|" + possible_states[0]
    third = possible_states[1] + "|" + possible_states[1]
    fourth = possible_states[0] + "|" + possible_states[1]

    # initializes values that will be incremented later
    count_first_state = 0
    count_second_state = 0

    first_first = 0
    second_first = 0
    second_second = 0
    first_second = 0

    char_counter = 0
    for char in string_sequence[0:len(string_sequence)-1]:
        if char_counter == 0:
            if char == possible_states[0]:
                computed_state_probab_dict[possible_states[0]].append(1)
                computed_state_probab_dict[possible_states[1]].append(0)
            elif char == possible_states[1]:
                computed_state_probab_dict[possible_states[0]].append(0)
                computed_state_probab_dict[possible_states[1]].append(1)

        if char == possible_states[0]:
            count_first_state += 1
            if possible_states[0] == string_sequence[char_counter+1]:
                first_first += 1
            elif possible_states[1] == string_sequence[char_counter+1]:
                second_first += 1
        elif char == possible_states[1]:
            count_second_state += 1
            if possible_states[0] == string_sequence[char_counter+1]:
                first_second += 1
            elif possible_states[1] == string_sequence[char_counter+1]:
                second_second += 1

        char_counter += 1
    
    # calculates for the transition probabilities
    first_value = first_first/count_first_state
    second_value = second_first/count_first_state
    third_value = second_second/count_second_state
    fourth_value = first_second/count_second_state

    # stores them into a dictionary
    computed_probabilities = {
        first: first_value,
        second: second_value,
        third: third_value,
        fourth: fourth_value
    }

    print("transition probabilities", computed_probabilities)

    return computed_probabilities, computed_state_probab_dict

def compute_state_probability(computing_str1, x, computed_probabilities_dict, computed_state_probab_dict, possible_states):
    unused = ""
    for char in possible_states:
        if char != computing_str1:
            unused = char
            break

    # sets the strings to be used later to reference dictionary values
    dict_key_1 = computing_str1 + "|" + possible_states[0]
    dict_key_2 = computing_str1 + "|" + possible_states[1]
    
    # calculates for the values while considering if the current value is already available to be computed
    counter = len(computed_state_probab_dict[possible_states[1]])-1
    while counter < x:
        # print(Iteration 1: )
        # print(computed_probabilities_dict[dict_key_1])
        # print(computed_state_probab_dict[possible_states[0]])
        # print(computed_probabilities_dict[dict_key_2])
        # print(computed_state_probab_dict[possible_states[1]])
        new_computed_value = (computed_probabilities_dict[dict_key_1] * computed_state_probab_dict[possible_states[0]][counter]) + (computed_probabilities_dict[dict_key_2] * computed_state_probab_dict[possible_states[1]][counter])
        computed_state_probab_dict[computing_str1].append(new_computed_value)
        computed_state_probab_dict[unused].append(1-new_computed_value)
        counter += 1
    
    print(computing_str1)
    print(computed_state_probab_dict[computing_str1])
    print(unused)
    print(computed_state_probab_dict[unused])
    return computed_state_probab_dict

def compute_final_value(x, computed_probabilities_dict, computed_state_probab_dict, computing_str1, computing_str2, possible_states, given_probabilities_dict):
    computed_state_probab_dict = compute_state_probability(computing_str1, x, computed_probabilities_dict, computed_state_probab_dict, possible_states)

    # sets the strings to be used later to reference dictionary values
    dict_key_1 = computing_str2 + "|" + possible_states[0]
    dict_key_2 = computing_str2 + "|" + possible_states[1]
    final_key = computing_str2 + "|" + computing_str1

    print(dict_key_1, ":", given_probabilities_dict[dict_key_1])
    print(possible_states[0], ":",  computed_state_probab_dict[possible_states[0]][x])
    print(dict_key_2, ":",  given_probabilities_dict[dict_key_2])
    print(possible_states[1], ":",  computed_state_probab_dict[possible_states[1]][x])

    # computes for the necessary values using the formula
    computed_value = (given_probabilities_dict[dict_key_1] * computed_state_probab_dict[possible_states[0]][x]) + (given_probabilities_dict[dict_key_2] * computed_state_probab_dict[possible_states[1]][x])
    final_value = (given_probabilities_dict[final_key] * computed_state_probab_dict[computing_str1][x]) / computed_value
    print("computed_value :", computed_value)
    print("final value :", final_value)
    return final_value

#======================================================================================================================================
original, number_of_strings, input_strings, possible_states, possible_measurements, probability_array, number_of_cases, formatted_array, numbers_array = readFile()
# Initialize the output content
output_content = []

i = 0
while i < number_of_strings:
    print("String #", i+1)
    print(input_strings[i])
    output_content.append(input_strings[i])
    string_sequence = input_strings[i]
    given_probabilities_dict, first_measurement_probab_array, second_measurement_probab_array = given_probabilities(possible_states, possible_measurements, probability_array)
    computed_probabilities_dict, computed_state_probab_dict = computed_probabilities(possible_states, string_sequence)
    j = 0
    while j < number_of_cases:
        print(original[j])
        computing_str1 = formatted_array[j][0]
        computing_str2 = formatted_array[j][1]
        x = numbers_array[j]
        print("Case #", j+1)
        result = compute_final_value(x, computed_probabilities_dict, computed_state_probab_dict, computing_str1, computing_str2, possible_states, given_probabilities_dict)
        result_rounded = round(result, 4)
        print("rounded off:", result_rounded)
        output_content.append(f"{original[j]} = {result_rounded}")
        print("-------------------------------------")
        j += 1
    print("==========================================================")
    i += 1

# Write the output to hmm.out
with open('hmm.out', 'w') as out_file:
    out_file.write('\n'.join(output_content))
#======================================================================================================================================