from django import template

register = template.Library()


@register.filter
def wall_material(material, obj):
    for _ in obj.project["wall"]:
        if isinstance(obj.project["wall"][material], dict):
            return material


@register.filter
def roof_material(material, obj):
    for _ in obj.project["roofbase"]:
        if isinstance(obj.project["roofbase"][material], dict):
            return material


@register.filter
def floor_material(material, obj):
    for _ in obj.project["floor"]:
        if isinstance(obj.project["floor"][material], dict):
            return material


@register.filter
def filter_material_if_changed(material, comparison_dict):
    for item in comparison_dict:
        for counter in range(len(comparison_dict[item])):
            if material in comparison_dict[item][counter].keys():
                return material


@register.filter
def divide(value, arg):
    return int(value) / int(arg)
