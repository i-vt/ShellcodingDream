import re
import argparse

def extract_and_split_bloated_code(bloated):
    bloated_lines = bloated.splitlines()
    header_lines = []
    rest_lines = []
    found_non_header = False

    for line in bloated_lines:
        if not found_non_header and line.strip().startswith("#include"):
            header_lines.append(line.strip())
        else:
            found_non_header = True
            rest_lines.append(line)

    rest_code = "\n".join(rest_lines)
    main_split = rest_code.split("int main() {", 1)

    if len(main_split) != 2:
        raise Exception("Could not split bloated main() properly")

    out_main_slop = main_split[0].strip()
    in_main_slop = main_split[1].rsplit("return 0;", 1)[0].strip()

    return "\n".join(header_lines), out_main_slop, in_main_slop


def extract_headers(code):
    pattern = r'#include\s+[<"].+[>"][^\n]*'
    matches = re.findall(pattern, code)
    seen = set()
    ordered_headers = []
    for header in matches:
        if header not in seen:
            ordered_headers.append(header)
            seen.add(header)
    return ordered_headers


def remove_headers(code):
    return re.sub(r'#include\s+[<"].+[>"]\s*', '', code)


def find_main_block(code):
    """Finds main() start and end using brace counting."""
    match = re.search(r"int\s+main\s*\([^)]*\)\s*{", code)
    if not match:
        raise Exception("main() not found")

    start = match.start()
    brace_count = 0
    i = match.end() - 1

    while i < len(code):
        if code[i] == '{':
            brace_count += 1
        elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return start, i + 1
        i += 1

    raise Exception("Matching closing brace for main() not found")


def merge_bloat_into_main(bloated, main_code):
    bloat_headers, out_main, in_main = extract_and_split_bloated_code(bloated)

    bloat_headers_list = extract_headers(bloat_headers)
    main_headers_list = extract_headers(main_code)

    # Preserve order from main, add only non-duplicates from bloat
    main_headers_set = set(main_headers_list)
    unique_bloat_headers = [h for h in bloat_headers_list if h not in main_headers_set]
    all_headers = main_headers_list + unique_bloat_headers

    # Remove headers from both bloat and main
    cleaned_main = remove_headers(main_code)

    # Find and replace main()
    main_start, main_end = find_main_block(cleaned_main)
    main_before = cleaned_main[:main_start]
    main_after = cleaned_main[main_end:]

    # Get the main declaration line to preserve signature
    main_decl = re.search(r"(int\s+main\s*\([^)]*\)\s*{)", cleaned_main[main_start:]).group(1)

    # Rebuild main
    new_main = f"{main_decl}\n{in_main}\n    return 0;\n}}"

    # Merge everything
    merged = "\n".join(all_headers) + "\n\n" + out_main + "\n\n" + main_before + new_main + main_after
    return merged


def main():
    parser = argparse.ArgumentParser(description="Merge bloated C code into a clean main file.")
    parser.add_argument('--bloated', required=True, help="Path to bloated C file")
    parser.add_argument('--main', required=True, help="Path to clean main C file")
    parser.add_argument('--output', required=True, help="Path to output merged C file")

    args = parser.parse_args()

    with open(args.bloated, "r") as f:
        bloated_code = f.read()

    with open(args.main, "r") as f:
        main_code = f.read()

    merged_output = merge_bloat_into_main(bloated_code, main_code)

    with open(args.output, "w") as f:
        f.write(merged_output)

if __name__ == "__main__":
    main()

