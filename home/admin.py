from django.contrib import admin
# from django.utils.decorators import admin
from home.models import Routine,Fixed_routine,Needed,preferred_routine

admin.site.register(Routine)
admin.site.register(Fixed_routine)
admin.site.register(Needed)
admin.site.register(preferred_routine)
