from manim import *


class LabeledNode(VGroup):
    def __init__(self, label, radius=0.25, color=BLUE):
        super().__init__()
        self.circle = Circle(radius=radius).set_fill(color, 1).set_stroke(BLACK, 2)
        self.text = Text(str(label)).scale(0.4)
        self.add(self.circle, self.text)
        self.label = label
        self.left = None
        self.right = None
        self.pos = np.array([0, 0, 0])

    def highlight(self, color=YELLOW):
        return self.circle.animate.set_fill(color)

    def reset(self, color=BLUE):
        return self.circle.animate.set_fill(color)


class BinaryTreeMobject(VGroup):
    def __init__(self, depth=3, node_color=BLUE, h_spacing=1.0, v_spacing=1.2):
        super().__init__()
        self.depth = depth
        self.node_color = node_color
        self.h_spacing = h_spacing
        self.v_spacing = v_spacing
        self.edges = VGroup()
        self.nodes = []

        self.root = self._build_tree(depth)
        self._assign_positions(self.root, 0, 2**depth - 1, 0)
        self._create_edges(self.root)
        self.tree_group = VGroup(self.edges, *self.nodes)
        self.add(self.tree_group)
        self._fit_to_frame()

    def _build_tree(self, level):
        if level < 0:
            return None
        node = LabeledNode(len(self.nodes) + 1, color=self.node_color)
        self.nodes.append(node)
        node.left = self._build_tree(level - 1)
        node.right = self._build_tree(level - 1)
        return node

    def _assign_positions(self, node, x_min, x_max, level):
        """Assign positions recursively. Leaves are evenly spaced horizontally."""
        if node is None:
            return
        x = (x_min + x_max) / 2
        y = -level * self.v_spacing
        node.pos = np.array([x, y, 0])
        self._assign_positions(node.left, x_min, x, level + 1)
        self._assign_positions(node.right, x, x_max, level + 1)

    def _create_edges(self, node):
        if node is None:
            return
        for child in (node.left, node.right):
            if child is not None:
                self.edges.add(Line(node.pos, child.pos, color=GREY))
                self._create_edges(child)

    def _fit_to_frame(self):
        """Scale and center the tree."""
        if not self.nodes:
            return
        x_coords = [n.pos[0] for n in self.nodes]
        width = max(x_coords) - min(x_coords) + 1
        scale = config.frame_width * 0.8 / width
        self.tree_group.scale(scale)
        self.tree_group.move_to(ORIGIN)

    # Public API
    def get_leaves(self):
        return [n for n in self.nodes if n.left is None and n.right is None]

    def traverse_inorder(self):
        result = []

        def inorder(node):
            if node is None:
                return
            inorder(node.left)
            result.append(node)
            inorder(node.right)

        inorder(self.root)
        return result


class TreeDemo(Scene):
    def construct(self):
        tree = BinaryTreeMobject(depth=3)
        self.play(Create(tree.edges))
        self.play(LaggedStart(*[GrowFromCenter(n) for n in tree.nodes], lag_ratio=0.1))
        self.wait()

        # Highlight inorder traversal
        for node in tree.traverse_inorder():
            self.play(node.highlight(), run_time=0.3)
            self.play(node.reset(), run_time=0.3)

        # Highlight leaves
        leaves = tree.get_leaves()
        self.play(*[leaf.highlight(GREEN) for leaf in leaves])
        self.wait(1)
