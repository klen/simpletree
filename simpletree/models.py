import sys

from django.db import models, connection
from django.utils.translation import ugettext_lazy as _

from .utils import commit_raw_sql


qn = connection.ops.quote_name


class NodeMeta(models.Model.__metaclass__):

    def __new__(mcs, class_name, bases, class_dict):
        """ Dynamicly create m2m relation.
        """
        meta = class_dict.get('Meta')
        if (meta and meta.abstract):
            return super(NodeMeta, mcs).__new__(mcs, class_name, bases, class_dict)

        class_module = class_dict['__module__']
        relation_module = sys.modules[class_module]
        relation_name = "{0}NodeMeta".format(class_name)
        relation_app_label = relation_module.__name__.split('.')[-2]

        class RelationMeta:
            unique_together = 'parent', 'child'

        relation_model = type(
            relation_name,
            (models.Model,),
            dict(
                __module__=class_module,
                parent=models.ForeignKey(
                    '{0}.{1}'.format(relation_app_label, class_name),
                    related_name='_child_links'),
                child=models.ForeignKey(
                    '{0}.{1}'.format(relation_app_label, class_name),
                    related_name='_parent_links'),
                depth=models.PositiveIntegerField(default=0),
                Meta=RelationMeta,
                __repr__=lambda s: "{0}/{1} [{2}]".format(
                    s.parent_id, s.child_id, s.depth)
            ))

        class_dict['{0}_child_set'.format(class_name.lower())] = models.ManyToManyField(
            'self',
            through='{0}.{1}'.format(relation_app_label, relation_name),
            symmetrical=False,
            related_name='{0}_parent_set'.format(class_name.lower())
        )
        class_dict['_relation_model'] = relation_model
        return super(NodeMeta, mcs).__new__(mcs, class_name, bases, class_dict)


class Node(models.Model):

    __metaclass__ = NodeMeta

    parent = models.ForeignKey(
        'self', null=True, blank=True, verbose_name=_("Parent node"))

    def __init__(self, *args, **kwargs):
        """ Precache parent value.
        """
        super(Node, self).__init__(*args, **kwargs)
        self.__parent = Node.parent.field.value_from_object(self)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        """ Update tree data
        """
        created = not self.pk

        super(Node, self).save(**kwargs)

        if created:
            self._relation_model.objects.create(parent=self, child=self)

        if self.parent_id != self.__parent:
            if not created:
                self.clean_tree(write=False)
            self.fix_tree()
            self.__parent = self.parent_id

    def delete(self, **kwargs):
        """ Delete links on self.
        """
        self.clean_tree()
        super(Node, self).delete(**kwargs)

    @commit_raw_sql
    def fix_tree(self):
        return """
            INSERT INTO {table}(parent_id, child_id, depth)
            SELECT a.parent_id, b.child_id, a.depth + b.depth + 1
            FROM {table} a, {table} b
            WHERE a.child_id = {parent} and b.parent_id = {child}"""\
        .strip().format(
            table=qn(self._relation_model._meta.db_table),
            parent=self.parent_id,
            child=self.pk)

    @commit_raw_sql
    def clean_tree(self):
        return """
            DELETE FROM {table} WHERE id IN (
                SELECT meta.id FROM {table} a, {table} meta, {table} b
                WHERE a.parent_id = meta.parent_id and b.child_id = meta.child_id and a.child_id = {parent} and b.parent_id = {child}
            )"""\
        .strip().format(
            table=qn(self._relation_model._meta.db_table),
            parent=self.parent_id,
            child=self.pk)

    def get_tree(self):
        return self.__class__.objects.filter(
            models.Q(_child_links__child=self) | models.Q(_parent_links__parent=self)
        ).distinct()


# pymode:lint_ignore=E1123
