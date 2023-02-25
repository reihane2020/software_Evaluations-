from django.db import models

# Create your models here.
class CommentReply(models.Model):
    user = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    parent = models.ForeignKey(
        "comment_evaluation.CommentEvaluateResult",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    content = models.TextField(default='')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']