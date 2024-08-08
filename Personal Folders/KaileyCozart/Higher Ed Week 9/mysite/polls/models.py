from django.db import models

# Create your models here.
class VolunteerInfo(models.Model):
    GTID = models.CharField(max_length=9, unique=True)
    email = models.EmailField()
    has_previously_applied = models.BooleanField()
    is_potential_volunteer = models.BooleanField()
    has_gpu = models.BooleanField()
    gpu_type = models.CharField(max_length=100, blank=True, null=True)
    has_research_xp = models.BooleanField()
    num_months_interested = models.IntegerField()
    has_used_pace = models.BooleanField()
    months_previously_volunteered = models.IntegerField()
    classes_taken = models.CharField(max_length=200, blank=True, null=True)
    programming_languages = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.GTID}"