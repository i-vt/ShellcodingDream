import random
import argparse

# Function to generate a random C variable name, with a length between 25 and 30 characters
def random_var_name(existing_names):
    while True:
        var_name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(25, 30)))
        if var_name not in existing_names:
            existing_names.add(var_name)
            return var_name

# Function to generate a random C data type
def random_data_type():
    return random.choice(['int', 'float', 'double'])

# Function to generate a random C expression using a declared variable
def random_expression(var, var_type):
    if var_type == 'int':
        op = random.choice(['+', '-', '*', '/', '%'])
    else:
        op = random.choice(['+', '-', '*', '/'])  # No modulus for float/double
    
    num = random.randint(1, 100)
    return f"{var} = {var} {op} {num};"

# Function to generate a random for loop using a declared variable
def random_for_loop(var):
    limit = random.randint(5, 50)
    return f"for(int {var} = 0; {var} < {limit}; {var}++) {{\n    printf(\"%d\\n\", {var});\n}}"

# Function to generate a random if statement using a declared variable
def random_if_statement(var):
    condition = random.choice([f"{var} > 0", f"{var} == 0", f"{var} < 10"])
    return f"if ({condition}) {{\n    printf(\"Condition met\\n\");\n}}"

# Function to generate a random comment
def random_comment():
    comment_length = random.randint(5, 15)  # Random length for comment
    words = [''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(2, 5))) for _ in range(comment_length)]
    return "// " + ' '.join(words)

# Function to generate a random standalone function definition with a unique name
def random_function(existing_names):
    func_name = random_var_name(existing_names)
    param_name = random_var_name(existing_names)
    return_type = random_data_type()
    comment = random_comment() if random.random() < 0.5 else ""  # Insert a random comment sometimes
    return func_name, f"{comment}\n{return_type} {func_name}({return_type} {param_name}) {{\n    {random_expression(param_name, return_type)}\n    return {param_name};\n}}\n"

# Function to generate the main function code
def generate_main_function(declared_vars, defined_functions, num_statements, existing_names):
    main_code = []
    main_code.append("int main() {\n")
    
    # Generate random variable declarations
    for var_name, data_type in declared_vars:
        comment = random_comment() if random.random() < 0.5 else ""  # Insert a random comment sometimes
        main_code.append(f"{comment}\n    {data_type} {var_name} = {random.randint(0, 100)};\n")
    
    # Add random expressions, loops, and if-statements using declared variables
    for _ in range(num_statements):
        var_name, var_type = random.choice(declared_vars)
        comment = random_comment() if random.random() < 0.5 else ""  # Insert a random comment sometimes
        main_code.append(f"{comment}\n    {random_expression(var_name, var_type)}\n")
        main_code.append(f"{comment}\n    {random_for_loop(var_name)}\n")
        main_code.append(f"{comment}\n    {random_if_statement(var_name)}\n")
    
    # Call some of the previously defined functions
    for func_name, _ in defined_functions:
        var_name, var_type = random.choice(declared_vars)
        main_code.append(f"    {var_type} result_{func_name} = {func_name}({var_name});\n")
    
    main_code.append("    return 0;\n")
    main_code.append("}\n")
    
    return ''.join(main_code)

# Function to generate the full C program by breaking code into functions with unique names
def generate_random_c_code(num_functions, num_vars, num_statements):
    code = []
    code.append("#include <stdio.h>\n")
    code.append("#include <stdlib.h>\n")
    code.append("#include <math.h>\n")
    code.append("#include <complex.h>\n\n")  # Include complex.h to handle complex-related functions
    
    # Track defined functions and declared variables
    defined_functions = []
    declared_vars = []
    
    # Set to track unique function and variable names
    existing_names = set()
    
    # Generate some random function definitions with unique names
    for _ in range(num_functions):
        func_name, func_code = random_function(existing_names)
        defined_functions.append((func_name, func_code))
        code.append(func_code)
    
    # Generate some random variable declarations for main with unique names
    for _ in range(num_vars):
        var_name = random_var_name(existing_names)
        data_type = random_data_type()
        declared_vars.append((var_name, data_type))
    
    # Add the main function code
    code.append(generate_main_function(declared_vars, defined_functions, num_statements, existing_names))
    
    return ''.join(code)

# Write the generated C code to a file
def write_c_code_to_file(filename, num_functions, num_vars, num_statements):
    c_code = generate_random_c_code(num_functions, num_vars, num_statements)
    with open(filename, 'w') as f:
        f.write(c_code)
    print(f"Random C code has been written to {filename}")

# Main function to parse arguments and generate code
def main():
    # Argument parsing using argparse
    parser = argparse.ArgumentParser(description='Generate random C code with functions, variables, and statements.')
    
    # Adding arguments for functions, variables, statements, and output filename
    parser.add_argument('--funs', '-f', type=int, default=random.randint(10,201), help='Number of functions to generate (default: 10 to 200)')
    parser.add_argument('--vars', '-v', type=int, default=random.randint(15,301), help='Number of variables to generate (default: 15 to 300)')
    parser.add_argument('--stms', '-s', type=int, default=random.randint(20,401), help='Number of statements to generate (default: 20 to 400)')
    parser.add_argument('--out', '-o', type=str, default='random_code.c', help='Output filename (default: random_code.c)')

    # Parse the arguments
    args = parser.parse_args()

    # Write the generated code to the specified file
    write_c_code_to_file(args.out, args.funs, args.vars, args.stms)

# Run the main function to take command-line arguments and generate code
if __name__ == "__main__":
    main()
