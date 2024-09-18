import math
import argparse

def open_file(string):
    with open(string, "r") as file:
        return file.read()

def entropy(string):
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def entropy_ideal(length):
    prob = 1.0 / length
    return -1.0 * length * prob * math.log(prob) / math.log(2.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Shannon entropy of a file")
    parser.add_argument("filename", help="The file to analyze")
    args = parser.parse_args()

    file_content = open_file(args.filename)
    print(entropy(file_content))
