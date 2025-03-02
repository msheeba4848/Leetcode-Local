# leetcode_local/cli/commands.py
import argparse
import os
import sys
import inspect
import time
from ..problems import arrays_and_hashing, two_pointers, sliding_window
from ..testing.test_runner import load_solution, run_test, print_test_results
from ..problems import Difficulty
from ..config.manager import get_config
from ..utils.solution_template import create_solution_template
from ..utils.problem_utils import get_problem_by_id, get_problem_by_name


# Dictionary mapping modules to their problem types
PROBLEM_MODULES = {
    "arrays_and_hashing": arrays_and_hashing,
    "two_pointers": two_pointers,
    "sliding_window": sliding_window,
    #"stack": stack,
    #"binary_search": binary_search,
    # Add other modules as they're implemented
}

def get_all_problems():
    """Get all problems from all modules."""
    problems = []
    for module_name, module in PROBLEM_MODULES.items():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'id') and hasattr(attr, 'title'):
                problems.append(attr)
    
    # Filter to LeetCode 75 if configured
    config = get_config()
    if config.get("leetcode75", "restrict_to_leetcode75", True):
        # In a real implementation, you'd have a way to identify which problems are part of LeetCode 75
        # For now, we'll just assume all problems are included
        pass
        
    return problems

def get_problem_by_id(problem_id):
    """Get a problem object by its ID."""
    try:
        problem_id = int(problem_id)
    except ValueError:
        return None
        
    for module_name, module in PROBLEM_MODULES.items():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'id') and attr.id == problem_id:
                return attr
    return None

def get_problem_by_name(problem_name):
    """Get a problem object by its name (case insensitive)."""
    for module_name, module in PROBLEM_MODULES.items():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'title') and attr.title.lower() == problem_name.lower():
                return attr
    return None

def main():
    parser = argparse.ArgumentParser(description="LeetCode Local Practice Tool")
    
    # Global options
    parser.add_argument("--config", help="Path to custom config file")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available problems")
    list_parser.add_argument("--category", help="Filter problems by category (e.g., arrays_and_hashing, binary_search)")
    list_parser.add_argument("--difficulty", choices=["EASY", "MEDIUM", "HARD", "ALL"], help="Filter problems by difficulty")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test your solution against a problem")
    test_parser.add_argument("problem", help="Problem ID or title")
    test_parser.add_argument("solution", help="Path to your solution file")
    test_parser.add_argument("--test-case", type=int, help="Run specific test case by index")
    test_parser.add_argument("--timeout", type=float, help="Maximum execution time for each test (seconds)")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a solution template")
    create_parser.add_argument("problem", help="Problem ID or title")
    create_parser.add_argument("--output", help="Output file path")
    create_parser.add_argument("--style", choices=["basic", "detailed"], help="Template style")
    
    # Random problem command
    random_parser = subparsers.add_parser("random", help="Get a random problem")
    random_parser.add_argument("--difficulty", choices=["EASY", "MEDIUM", "HARD", "ALL"], help="Filter by difficulty")
    random_parser.add_argument("--category", help="Filter by problem category")
    
    # Browse problems command
    browse_parser = subparsers.add_parser("browse", help="Browse problems interactively")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("action", choices=["show", "create", "set", "reset"], help="Config action")
    config_parser.add_argument("--section", help="Configuration section (for 'set' action)")
    config_parser.add_argument("--key", help="Configuration key (for 'set' action)")
    config_parser.add_argument("--value", help="Configuration value (for 'set' action)")
    config_parser.add_argument("--path", help="Path to create/save configuration")
    
    args = parser.parse_args()
    
    # Initialize configuration
    if args.config:
        from ..config.manager import ConfigManager
        global_config = ConfigManager(args.config)
    else:
        global_config = get_config()
    
    if args.command == "list":
        difficulty = args.difficulty if args.difficulty and args.difficulty != "ALL" else None
        list_problems(args.category, difficulty)
    elif args.command == "test":
        timeout = args.timeout or global_config.get("testing", "timeout", 5)
        test_solution(args.problem, args.solution, args.test_case, timeout)
    elif args.command == "create":
        style = args.style or global_config.get("preferences", "template_style", "detailed")
        create_solution_template(args.problem, args.output, style)
    elif args.command == "random":
        difficulty = args.difficulty if args.difficulty and args.difficulty != "ALL" else None
        get_random_problem(difficulty, args.category)
    elif args.command == "browse":
        browse_problems_interactive()
    elif args.command == "config":
        manage_config(args)
    else:
        parser.print_help()
def test_solution(problem_id, solution_path, test_case_idx=None, timeout=5):
    """Runs the solution and prints results using your test runner."""
    problem = get_problem_by_id(problem_id)

    if not problem:
        print(f"Problem with ID {problem_id} not found.")
        return

    try:
        solution_func = load_solution(solution_path, problem.function_name)
        results = run_test(problem, solution_func, test_case_idx)
        print_test_results(problem, results)
    except Exception as e:
        print(f"Error while running tests: {e}")

def list_problems(category=None, difficulty=None):
    """List available problems, optionally filtered by category and/or difficulty."""
    print("Available LeetCode problems:")
    
    config = get_config()
    problems = get_all_problems()
    
    # Apply filters
    if category:
        problems = [p for p in problems if p.category.lower() == category.lower()]
    if difficulty:
        difficulty_enum = Difficulty[difficulty]
        problems = [p for p in problems if p.difficulty == difficulty_enum]
    
    # Sort by ID
    problems.sort(key=lambda p: p.id)
    
    # Count problems by difficulty
    easy_count = sum(1 for p in problems if p.difficulty == Difficulty.EASY)
    medium_count = sum(1 for p in problems if p.difficulty == Difficulty.MEDIUM)
    hard_count = sum(1 for p in problems if p.difficulty == Difficulty.HARD)
    
    # Count problems by category
    categories = {}
    for p in problems:
        if p.category not in categories:
            categories[p.category] = 0
        categories[p.category] += 1
    
    # Print summary
    print(f"\nTotal: {len(problems)} problems")
    print(f"Difficulty breakdown: {easy_count} Easy, {medium_count} Medium, {hard_count} Hard")
    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} problems")
    
    # Get colors from config
    color_easy = config.get("problems", "color_easy", "green")
    color_medium = config.get("problems", "color_medium", "yellow")
    color_hard = config.get("problems", "color_hard", "red")
    
