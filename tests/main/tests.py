from django.test import TestCase
from milkman.dairy import milkman


class TreeTestCase(TestCase):

    def test_models(self):
        from .models import Page
        self.assertFalse(Page.objects.count())

        root = milkman.deliver(Page)
        page11 = milkman.deliver(Page, parent=root)
        page12 = milkman.deliver(Page, parent=root)
        page21 = milkman.deliver(Page, parent=page11)
        page31 = milkman.deliver(Page, parent=page21)

        # Move tree
        page21.parent = page12
        page21.save()
