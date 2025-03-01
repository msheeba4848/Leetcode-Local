import inspect
import importlib.util
import sys
import os
from typing import Callable, List, Dict, Any

def load_solution(file_path: str, function_name: str) -> Callable:
    """Load a solution function from a Python file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Solution file not found: {file_path}")
    
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    if not hasattr(module, function_name):
        raise AttributeError(f"Function '{function_name}' not found in {file_path}")
    
    return getattr(module, function_name)

def run_test(problem, solution_func, test_case_idx=None):
    """Run tests for a solution against a problem's test cases."""
    results = []
    test_cases = problem.examples
    
    if test_case_idx is not None:
        if 0 <= test_case_idx < len(test_cases):
            test_cases = [test_cases[test_case_idx]]
        else:
            raise IndexError(f"Test case index {test_case_idx} out of range")
    
    for i, test_case in enumerate(test_cases):
        # Deep copy to avoid modifying original test case
        input_data = test_case["input"].copy()
        expected_output = test_case["output"]
        
        try:
            # Convert dict-based input to function parameters
            actual_output = solution_func(**input_data)
            
            # Compare outputs
            passed = actual_output == expected_output
            
            results.append({
                "test_case_idx": i,
                "input": input_data,
                "expected": expected_output,
                "actual": actual_output,
                "passed": passed
            })
        except Exception as e:
            results.append({
                "test_case_idx": i,
                "input": input_data,
                "expected": expected_output,
                "actual": str(e),
                "passed": False,
                "error": str(e)
            })
    
    return results

def print_test_results(problem, results):
    """Print the results of testing a solution with friendly messages."""
    print(f"\n===== TESTING {problem.title} =====")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["passed"])
    
    for i, result in enumerate(results):
        if result["passed"]:
            print(f"You're correct! So proud of you! Test Case {result['test_case_idx'] + 1}")
            print(f"   Input: {result['input']}")
            print(f"   Output: {result['actual']}")
        else:
            print(f"Great work, you're almost there. You need to fix this! Test Case {result['test_case_idx'] + 1}")
            print(f"   Input: {result['input']}")
            print(f"   Expected: {result['expected']}")
            print(f"   Actual: {result['actual']}")
            if "error" in result:
                print(f"   Error: {result['error']}")

    print(f"\nSummary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("All tests passed! Your solution is correct.")
    else:
        print(f"{total_tests - passed_tests} test(s) failed. Keep trying!")
