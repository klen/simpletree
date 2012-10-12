from django.test import TestCase
import time
from .models import SimpleTree, MPTTTree, TBMP, TBNS


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '\n%r: %2.2f sec' % \
              (method.__name__, te - ts)
        return result

    return timed


CYCLES = 8


class Benchmark(object):

    @timeit
    def test_creation(self):
        self._create_tree()

    def test_delete(self):
        self._create_tree(cycles=7)

        @timeit
        def test_deletion():
            for _ in xrange(pow(2, CYCLES) / 2):
                self._delete_last()
        test_deletion()

    # def test_get(self):
        # self._create_tree(cycles=7)

        # @timeit
        # def test_get_tree():
            # root = self._get_root()
            # for _ in xrange(100):
                # self._get_tree(root)
        # test_get_tree()

    def _create_tree(self, cycles=CYCLES):
        root = self._create_root(title='root1')
        nodes = [root]
        for _ in xrange(CYCLES):
            new_nodes = []
            for node in nodes:
                new_nodes.append(self._create_child(parent=node))
                new_nodes.append(self._create_child(parent=node))
            nodes = new_nodes

        return nodes

    def _create_root(self, **params):
        pass

    def _create_child(self, parent, **params):
        pass

    def _delete_last(self):
        pass

    def _get_root(self):
        pass

    def _get_tree(self, parent):
        pass


class SimpleTest(TestCase, Benchmark):

    def setUp(self):
        print "\nSimpleTree benchmark"

    def _create_root(self, **params):
        return SimpleTree.objects.create(**params)

    def _create_child(self, parent, **params):
        return SimpleTree.objects.create(parent=parent, **params)

    def _delete_last(self):
        SimpleTree.objects.order_by('-id')[0].delete()

    def _get_root(self):
        return SimpleTree.objects.get(parent=None)

    def _get_tree(self, parent):
        import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
        return parent.get_tree()


class MPTTTest(TestCase, Benchmark):

    def setUp(self):
        print "\nMPTT benchmark"

    def _create_root(self, **params):
        return MPTTTree.objects.create(**params)

    def _create_child(self, parent, **params):
        return MPTTTree.objects.create(parent=parent, **params)

    def _delete_last(self):
        MPTTTree.objects.order_by('-id')[0].delete()

    def _get_root(self):
        return MPTTTree.objects.get(parent=None)


class TreeBeardMP(TestCase, Benchmark):

    def setUp(self):
        print "\nTreebeard MP benchmark"

    def _create_root(self, **params):
        return TBMP.add_root(**params)

    def _create_child(self, parent, **params):
        return parent.add_child(**params)

    def _delete_last(self):
        TBMP.objects.order_by('-id')[0].delete()


class TreeBeardNS(TreeBeardMP):

    def setUp(self):
        print "\nTreebeard NS benchmark"

    def _create_root(self, **params):
        return TBNS.add_root(**params)

    def _delete_last(self):
        TBNS.objects.order_by('-id')[0].delete()
