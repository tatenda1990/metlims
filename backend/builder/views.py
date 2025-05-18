from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FormSchema, ClientSubmission
from .forms import build_dynamic_form
import json
from decimal import Decimal

def decimal_to_float(data):
    # Recursively convert Decimal instances to float
    if isinstance(data, dict):
        return {k: decimal_to_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float(i) for i in data]
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data

def get_form_definition(request, form_id):
    try:
        form = FormSchema.objects.get(pk=form_id)
        fields = list(form.fields.values())
        return JsonResponse({
            "form_name": form.name,
            "description": form.description,
            "fields": fields
        })
    except FormSchema.DoesNotExist:
        return JsonResponse({"error": "Form not found"}, status=404)

@csrf_exempt
def submit_form_data(request, form_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        ClientSubmission.objects.create(
            form_id=form_id,
            submission_data=data
        )
        return JsonResponse({"message": "Submission successful"})
    return JsonResponse({"error": "Invalid method"}, status=405)

def submit_form(request, form_id):
    form_schema = get_object_or_404(FormSchema, id=form_id)
    DynamicForm = build_dynamic_form(form_schema)

    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            cleaned_data = decimal_to_float(form.cleaned_data)
            submission = ClientSubmission.objects.create(
                form=form_schema,
                submission_data=cleaned_data,
            )
            return redirect('submit_form', form_id=form_schema.id) # Or wherever you want after submit
    else:
        form = DynamicForm()

    return render(request, 'submit_form.html', {'form': form, 'form_schema': form_schema})
