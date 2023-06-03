from django.db import models
from django.utils.translation import ugettext_lazy as _


class Fixed_routine(models.Model):
    data = models.TextField()

class Needed(models.Model):
    data = models.TextField()

class preferred_routine(models.Model):
    data = models.TextField()

#Routine store complete
class Routine(models.Model):
    tags = models.CharField(max_length=50)
    fixed_times = models.ForeignKey(Fixed_routine,on_delete=models.CASCADE, default="")
    needed_times = models.ForeignKey(Needed,on_delete=models.CASCADE,default="")
    preferred_times = models.ForeignKey(preferred_routine,on_delete=models.CASCADE,default="")
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now_add=True)


