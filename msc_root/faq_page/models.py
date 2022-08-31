from django.db import models


class FaqPage(models.Model):
    description = models.TextField('Questions')

    def __str__(self):
        return self.description
