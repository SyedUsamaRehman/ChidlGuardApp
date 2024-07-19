# # your_project/your_app/admin.py
# from django.contrib import admin
# # from django.contrib.admin import ModelAdmin
# from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
# from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
# from .models import Parent, Child, Csv_data
# from django.contrib.auth.models import User









# # Define inline for Csv_data
# class CsvDataInline(NestedTabularInline):
#     model = Csv_data
#     extra = 1

# # Define inline for Child with nested CsvDataInline
# class ChildInline(NestedStackedInline):
#     model = Child
#     extra = 1
#     inlines = [CsvDataInline]

# # Define inline for Parent with nested ChildInline
# class ParentAdmin(DefaultUserAdmin):
#     inlines = [ChildInline]

#     # Specify the fields to display on the list view
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
#     # Specify the fields to display in the form view
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     # Ensure that only the specified fields are displayed in the form
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2'),
#         }),
#     )

# # Register the custom user model
# admin.site.register(Parent, ParentAdmin)



# # Register other models
# admin.site.register(Child)  # Register Child if needed separately
# admin.site.register(Csv_data)  # Register Csv_data if needed separately
# # Customize the admin site headers
# admin.site.site_header = "ChildGuard"
# admin.site.site_title = "Child Guard"
# admin.site.index_title = "Welcome to Child Guard"



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
from .models import Parent, Child, Csv_data

# Define inline for Csv_data
class CsvDataInline(NestedTabularInline):
    model = Csv_data
    extra = 1

# Define inline for Child with nested CsvDataInline
class ChildInline(NestedStackedInline):
    model = Child
    extra = 1
    inlines = [CsvDataInline]

# Define a custom UserAdmin class to include ChildInline
class ParentAdmin(DefaultUserAdmin, NestedModelAdmin):
    inlines = [ChildInline]

    # Specify the fields to display on the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Specify the fields to display in the form view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Ensure that only the specified fields are displayed in the form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

# Register the custom user model
admin.site.register(Parent, ParentAdmin)

# # Register other models
# admin.site.register(Child)  # Register Child if needed separately
# admin.site.register(Csv_data)  # Register Csv_data if needed separately

# Customize the admin site headers
admin.site.site_header = "ChildGuard"
admin.site.site_title = "Child Guard"
admin.site.index_title = "Welcome to Child Guard"
