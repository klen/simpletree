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

# pymode:lint_ignore=F0401,W0612,W806
