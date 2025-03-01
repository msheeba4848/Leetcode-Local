from ..utils.problem_utils import get_problem_by_id, get_problem_by_name

def create_solution_template(problem_identifier, output_path=None, style="detailed"):
    """Create a solution template for a problem."""
    problem = get_problem_by_id(problem_identifier) or get_problem_by_name(problem_identifier)
    
    if not problem:
        print(f"Problem not found: {problem_identifier}")
        return
    
    if output_path is None:
        output_path = f"solution_{problem.id}_{problem.function_name}.py"
    
    with open(output_path, 'w') as f:
        f.write(f"""# LeetCode Problem {problem.id}: {problem.title}
# {problem.difficulty.name} - {problem.category}

\"\"\"
{problem.description.strip()}

Examples:
{chr(10).join(['  ' + str(ex['input']) + ' -> ' + str(ex['output']) for ex in problem.examples])}

Constraints:
{problem.constraints.strip()}
\"\"\"

def {problem.function_name}({', '.join(problem.examples[0]['input'].keys())}):
    # TODO: Implement your solution here
    pass


# Test your solution
if __name__ == "__main__":
    # Example test cases
    {chr(10).join(['    print(' + problem.function_name + '(**' + str(ex['input']) + '))  # Expected: ' + str(ex['output']) for ex in problem.examples])}
""")
    
    print(f"Solution template created at {output_path}")
    print(f"Edit the file and implement your solution for {problem.title}")