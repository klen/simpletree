from django.db import models

from simpletree.models import Node


class Page(Node):

    title = models.CharField(max_length=100)

    def __repr__(self):
        return "<Page {0}/{1}".format(self.pk, self.parent_id or '0')
