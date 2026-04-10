def reverse_string(s):
    reversed_s = ""
    for char in s:
        reversed_s = char + reversed_s
    return reversed_s


test_string = "Hello, World!"
print(reverse_string(test_string))