from django.db import models

# Create your models here.


class CommentEvaluate(models.Model):
    software = models.ForeignKey("software.Software", on_delete=models.CASCADE)
    section = models.ForeignKey(
        "software.SoftwareSection", on_delete=models.CASCADE,
    )
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "authentication.Account", on_delete=models.CASCADE
    )
    created_datetime = models.DateTimeField(auto_now=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.section in self.software.sections.all():
            pass
        else:
            raise Exception(
                "Selected section is not in sections of this software"
            )
        return super().save(*args, **kwargs)
