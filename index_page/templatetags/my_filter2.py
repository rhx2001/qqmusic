from django import template

register = template.Library()


@register.simple_tag
def tri_filter_back(dictionary, dic2, dic3, key):
    key = int(dic2[dic3][key])-1 if int(dic2[dic3][key]) > 0 else 19
    strs = f"{dictionary[key].get('song_name')}/{dictionary[key].get('singer')}/{dictionary[key].get('list_name')}"
    return strs

@register.simple_tag
def tri_filter_forward(dictionary, dic2, dic3, key):
    key = int(dic2[dic3][key])+1 if int(dic2[dic3][key]) < 19 else 0
    strs = f"{dictionary[key].get('song_name')}/{dictionary[key].get('singer')}/{dictionary[key].get('list_name')}"
    return strs