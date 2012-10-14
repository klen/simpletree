from django.test import TestCase
from milkman.dairy import milkman
from .models import Page


class TreeTestCase(TestCase):

    def setUp(self):
        """ Create test tree
        """
        root1 = milkman.deliver(Page)
        page11 = milkman.deliver(Page, parent=root1)
        page12 = milkman.deliver(Page, parent=root1)
        page111 = milkman.deliver(Page, parent=page11)
        page1111 = milkman.deliver(Page, parent=page111)
        page1112 = milkman.deliver(Page, parent=page111)

        self.__dict__.update(locals())

    def test_models(self):
        self.assertEqual(Page.objects.count(), 6)

    def test_get_root_nodes(self):
        self.assertEqual(list(Page.objects.filter(parent=None)), [self.root1])

    def test_get_tree(self):
        with self.assertNumQueries(1):
            pages = self.page11.get_tree()
            self.assertEqual(len(pages), 5)

    def test_api(self):

        # is root
        self.assertTrue(self.root1.is_root())
        self.assertFalse(self.page1112.is_root())

        # is leaf
        self.assertFalse(self.root1.is_leaf())
        self.assertTrue(self.page1112.is_leaf())

        # get_children
        self.assertEqual(
            list(self.page111.get_children()),
            [self.page1111, self.page1112]
        )

        # get_ancestors
        self.assertEqual(
            list(self.page111.get_ancestors()),
            [self.page111, self.page11, self.root1]
        )

        # get_descendants
        self.assertEqual(
            list(self.page111.get_descendants()),
            [self.page111, self.page1111, self.page1112]
        )

    def test_prefetch_related(self):
        with self.assertNumQueries(2):
            nodes = Page.objects.prefetch_related('node_descendants').filter(
                pk__in=[self.page11.pk, self.page12.pk]
            )
            self.assertTrue(list(nodes))
            self.assertEqual(len(nodes[0].node_descendants.all()), 4)


class BenchmarkTestCase(TestCase):

    def test_big_tree(self):
        root = Page.objects.create(title='root1')
        nodes = [root]
        for _ in xrange(4):
            new_nodes = []
            for node in nodes:
                new_nodes.append(Page.objects.create(parent=node))
                new_nodes.append(Page.objects.create(parent=node))
            nodes = new_nodes

        page = nodes[0]
        self.assertEqual(list(page.get_tree()), [
            page.parent.parent.parent.parent,
            page.parent.parent.parent,
            page.parent.parent,
            page.parent,
            page
        ])

        node = page.parent.parent
        page.parent.delete()
        self.assertFalse(Page.objects.filter(pk=page.pk).count())

        self.assertEqual(list(node.get_tree()), [
            node.parent.parent,
            node.parent,
            node,
        ] + list(node.get_descendants(exclude_self=True)))


# pymode:lint_ignore=F0401,W0612,W806
