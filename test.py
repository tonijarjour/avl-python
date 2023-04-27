import binarysearch
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.tree = binarysearch.Tree()

    def test(self):
        for n in range(1000):
            self.tree.insert(n)

        self.tree.remove(511)
        self.assertEqual(self.tree.position(511), None)

        root_index = self.tree.get_root()
        self.assertEqual(root_index, 511)
        self.assertEqual(self.tree.get_node(511), 512)

        for n in range(400, 600):
            self.tree.remove(n)

        self.assertEqual(self.tree.position(512), None)
        self.assertEqual(self.tree.position(499), None)

        for v in self.tree.iter(16):
            print(v)

        for n in range(1000):
            self.tree.remove(n)


if __name__ == "__main__":
    unittest.main()
