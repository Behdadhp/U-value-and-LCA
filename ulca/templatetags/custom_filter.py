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
