class Instance:
    def __init__(self, coefficients_matrix: list[list[float]], variable_subsets: list[set[int]]):
        self.coefficients_matrix = coefficients_matrix
        self.variable_subsets = variable_subsets

    @staticmethod
    def from_input_file(input_file_path: str) -> "Instance":
        with open(input_file_path, "r") as f:
            lines = f.readlines()
        n_variables = int(lines[0].strip())
        variable_subsets = []
        for line in lines[2:n_variables + 2]: # We skip the second line, which has the number of elements per subset
            subset = set([int(x) for x in line.strip().split()])
            variable_subsets.append(subset)

        coefficients_matrix = []
        for i, line in enumerate(lines[n_variables + 2:]):
            array_row = [float(x) for x in line.strip().split()]
            # Every line in the instance file corresponds to one row in a superior triangular matrix
            # Therefore the first i elements of the row are zeros
            pad_for_superior_triangular_matrix = [0] * i
            coefficients_matrix.append(pad_for_superior_triangular_matrix + array_row)
        return Instance(coefficients_matrix, variable_subsets)
    
    def __str__(self):
        result = "Instance(\n"
        result += "  coefficients_matrix:\n"
        result += '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.coefficients_matrix]) + "\n"
        result += "  variable_subsets:\n"
        for i, subset in enumerate(self.variable_subsets):
            result += f"    subset {i + 1}: " + " ".join(map(str, subset)) + "\n"
        result += ")"
        return result
