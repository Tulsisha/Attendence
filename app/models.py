from django.db import models
from django.conf import settings
from django.utils import timezone

class DailyAttendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    punch_in = models.TimeField(null=True, blank=True)
    punch_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')  # 🔒 ensures one record per user per date
        ordering = ['-date']  # 🗂 recent attendance first

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def status(self):
        """Optional: shows current attendance status"""
        if self.punch_in and not self.punch_out:
            return "Present (Not Punched Out)"
        elif self.punch_in and self.punch_out:
            return "Present"
        else:
            return "Absent"
