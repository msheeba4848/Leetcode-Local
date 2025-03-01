from ..problems import arrays_and_hashing, two_pointers, sliding_window

PROBLEM_MODULES = {
    "arrays_and_hashing": arrays_and_hashing,
    "two_pointers": two_pointers,
    "sliding_window": sliding_window,
    # Add more modules if needed
}

def get_problem_by_id(problem_id):
    try:
        problem_id = int(problem_id)
    except ValueError:
        return None

    for module in PROBLEM_MODULES.values():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'id') and attr.id == problem_id:
                return attr
    return None

def get_problem_by_name(problem_name):
    for module in PROBLEM_MODULES.values():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, 'title') and attr.title.lower() == problem_name.lower():
                return attr
    return None
