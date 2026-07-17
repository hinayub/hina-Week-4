from django.db import models


class ResearchQuery(models.Model):
    """A single research request and the agent's grounded answer."""

    query = models.TextField()
    answer = models.TextField(blank=True)
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Research queries"

    def __str__(self):
        return self.query[:80]
