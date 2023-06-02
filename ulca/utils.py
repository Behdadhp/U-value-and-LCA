def sort_project(instance):
    """Sort the project based on IDs before saving"""

    sorted_dict = {}
    for component in instance:
        sorted_component = {
            key: value
            for key, value in sorted(
                instance[component].items(),
                key=lambda x: x[1]["id"] if isinstance(x[1], dict) else float("inf"),
            )
        }
        sorted_dict[component] = sorted_component

    return sorted_dict
