# forms.py
from django import forms

def build_dynamic_form(form_schema):
    """
    Given a FormSchema instance, return a Django Form class
    with fields matching the FormFields.
    """
    fields = {}
    for field in form_schema.fields.all().order_by('order'):
        field_kwargs = {
            'label': field.label,
            'required': field.is_required,
        }

        if field.field_type == 'text':
            fields[field.key] = forms.CharField(**field_kwargs)
        elif field.field_type == 'number':
            fields[field.key] = forms.DecimalField(**field_kwargs)
        elif field.field_type == 'email':
            fields[field.key] = forms.EmailField(**field_kwargs)
        elif field.field_type == 'phone':
            fields[field.key] = forms.CharField(**field_kwargs)  # Could add validation here
        elif field.field_type == 'textarea':
            fields[field.key] = forms.CharField(widget=forms.Textarea, **field_kwargs)
        elif field.field_type == 'dropdown':
            choices = [(opt, opt) for opt in (field.options or [])]
            fields[field.key] = forms.ChoiceField(choices=choices, **field_kwargs)
        elif field.field_type == 'url':
            fields[field.key] = forms.URLField(**field_kwargs)
        # add more field types as needed

    return type('DynamicForm', (forms.Form,), fields)
