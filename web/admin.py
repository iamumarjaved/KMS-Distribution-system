from django.contrib import admin
from .models import *

admin.site.register(MyUser)
admin.site.register(Order)
admin.site.register(dir_connection)
admin.site.register(zone)
admin.site.register(zone_connection)
admin.site.register(order_sales)
admin.site.register(final_order)


# from django.contrib import admin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#
# from .forms import UserChangeForm, UserCreationForm
# from .models import User
#
#
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     list_display = ('email', 'phone', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('phone','type',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'phone', 'password1', 'password2')}
#          ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()
#
#
# admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)