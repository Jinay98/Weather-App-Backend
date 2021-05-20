from django.contrib import admin

from .models import AppUser


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'date_joined', 'last_login', 'is_admin')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("password",)
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form

    search_fields = ('phone_number', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()

    fieldsets = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(AppUser, UserAdmin)
