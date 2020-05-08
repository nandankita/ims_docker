from django import template
import json

register = template.Library()


@register.filter
def modelname(form):
    return form.__class__._meta.model._meta.object_name


@register.filter
def get_fields(obj):
    #return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]
    fields = []
    for f in obj._meta.fields:

        fname = f.name        
        # resolve picklists/choices, with get_xyz_display() function
        get_choice = 'get_'+fname+'_display'
        if hasattr(obj, get_choice):
            value = getattr(obj, get_choice)()
        else:
            try:
                value = getattr(obj, fname)
            except AttributeError:
                value = None

        # only display fields with values and skip some fields entirely
        if value and f.name not in ('id') :

            fields.append(
              {
               'label':f.verbose_name, 
               'name':f.name, 
               'value':value,
              }
            )
            
    return fields




@register.simple_tag
def json_saved_data(value):
   return (json.loads(value))
