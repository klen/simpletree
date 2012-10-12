from simpletree.models import Node
from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node
from treebeard.ns_tree import NS_Node
from django.db import models


class SimpleTree(Node):
    title = models.CharField(max_length=100, null=True)


class MPTTTree(MPTTModel):
    title = models.CharField(max_length=100, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')


class TBMP(MP_Node):
    title = models.CharField(max_length=100, null=True)


class TBNS(NS_Node):
    title = models.CharField(max_length=100, null=True)
