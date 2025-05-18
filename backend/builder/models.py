# models.py

from django.db import models
from django.utils.text import slugify
from django.db.models import Max


class FormSchema(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added for timestamp modification

    def __str__(self):
        return self.name


class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('textarea', 'Textarea'),
        ('dropdown', 'Dropdown'),
        ('url', 'Website URL'),  # Added website field
    ]

    form = models.ForeignKey(FormSchema, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    key = models.SlugField(max_length=255, blank=True, help_text="Used as the database field name.")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=True)
    is_unique = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    is_autoincrement = models.BooleanField(default=False)
    options = models.JSONField(blank=True, null=True, help_text="Required for dropdown fields.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = [('form', 'key')]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = slugify(self.label)
        if not self.order:
            max_order = FormField.objects.filter(form=self.form).aggregate(Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.field_type})"


from django.db import models
from django.db.models import Max

class ClientSubmission(models.Model):
    form = models.ForeignKey(FormSchema, on_delete=models.SET_NULL, null=True)
    submission_data = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Optional: track edits to submission

    def save(self, *args, **kwargs):
        if self.form:
            auto_fields = FormField.objects.filter(form=self.form, is_autoincrement=True)
            data = self.submission_data.copy()

            for field in auto_fields:
                key = field.key
                if key not in data or data[key] in [None, '', 0]:
                    max_value = ClientSubmission.objects.filter(form=self.form).aggregate(
                        Max(f'submission_data__{key}')
                    )[f'submission_data__{key}__max']
                    data[key] = (max_value or 0) + 1

            self.submission_data = data

        super().save(*args, **kwargs)

    def __str__(self):
        auto_fields = FormField.objects.filter(form=self.form, is_autoincrement=True)
        if auto_fields:
            fields_str = ", ".join(
                f"{field.label}: {self.submission_data.get(field.key, 'N/A')}"
                for field in auto_fields
            )
            return f"Submission ({fields_str}) for form '{self.form.name if self.form else 'Unknown'}'"
        return f"Submission #{self.id} for form '{self.form.name if self.form else 'Unknown'}'"

