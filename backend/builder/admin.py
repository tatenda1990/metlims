# admin.py

from django.contrib import admin
from .models import FormSchema, FormField, ClientSubmission


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    fields = (
        'label', 'key', 'field_type', 'is_required', 'is_unique',
        'is_primary', 'is_autoincrement', 'order', 'options'
    )
    ordering = ('order',)


@admin.register(FormSchema)
class FormSchemaAdmin(admin.ModelAdmin):
    inlines = [FormFieldInline]
    list_display = ['name', 'description', 'created_at', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(ClientSubmission)
class ClientSubmissionAdmin(admin.ModelAdmin):
    list_display = ['form', 'submitted_at']
    list_filter = ['form']
    readonly_fields = ['submission_data', 'submitted_at']
