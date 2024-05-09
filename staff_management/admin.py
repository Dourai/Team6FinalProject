from django.contrib import admin
from .models import Employee
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

# These are some customizations to the Django admin interface
admin.site.site_header = "Staff Management Admin Portal"
admin.site.site_title = "Staff Management Admin Portal"
admin.site.index_title = "Staff Management Admin Portal"

# We want to leverage Django's built-in admin interface to manage employees
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'tenure', 'department', 'wage', 'avg_hours_per_week')
    list_filter = ('department', 'name')
    search_fields = ('username', 'name')
    ordering = ('username',)
    fields = ('username', 'name', 'tenure', 'department', 'wage', 'avg_hours_per_week')

    # We only want superusers to be able to manage employees
    def has_module_permission(self, request):
        return request.user.is_superuser

    # We want to make a default password of 12345 for new employees
    def save_model(self, request, obj, form, change):
        if not change: # only set password for new employees
            obj.password = make_password('12345')
        super().save_model(request, obj, form, change)


# We don't want to use Django's built-in Group model
admin.site.unregister(Group)
