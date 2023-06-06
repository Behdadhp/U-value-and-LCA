def sort_project(instance, component):
    """Sort the project based on IDs before saving"""

    sorted_component = {
        key: value
        for key, value in sorted(
            instance[component].items(),
            key=lambda x: x[1]["id"] if isinstance(x[1], dict) else float("inf"),
        )
    }
    return sorted_component
