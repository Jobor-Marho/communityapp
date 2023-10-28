from django.contrib import admin
from censusapp.models import Adult, Child, Indigene, AdminUser

# Register your models here.
admin.site.register(Adult)
admin.site.register(Child)
admin.site.register(Indigene)
admin.site.register(AdminUser)



