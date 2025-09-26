from manim import *


class LabeledNode(VGroup):
    def __init__(self, label, radius=0.35, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius).set_fill(color, 1).set_stroke(BLACK, 2)
        self.text = Text(str(label)).scale(0.5)
        self.add(self.circle, self.text)
        self.label = label
        self.left = None
        self.right = None

    def highlight(self, color=YELLOW):
        return self.circle.animate.set_fill(color)

    def reset(self, color=BLUE):
        return self.circle.animate.set_fill(color)


class BinaryTreeMobject(VGroup):
    def __init__(self, depth=3, h_spacing=1.5, v_spacing=1.5, node_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.depth = depth
        self.h_spacing = h_spacing
        self.v_spacing = v_spacing
        self.node_color = node_color

        self.nodes = []  # list of all LabeledNode objects
        self.edges = VGroup()

        # Build tree
        self.root = self._build_tree(0)
        self._inorder_counter = 0
        self._assign_positions(self.root, 0)
        self._build_edges(self.root)
        self.tree_group = VGroup(self.edges, *self.nodes)
        self.add(self.tree_group)
        self._fit_to_frame()

    def _build_tree(self, level):
        if level > self.depth:
            return None
        node = LabeledNode(len(self.nodes) + 1, color=self.node_color)
        self.nodes.append(node)
        node.left = self._build_tree(level + 1)
        node.right = self._build_tree(level + 1)
        return node

    def _assign_positions(self, node, level):
        """Assign x and y positions recursively using in-order traversal."""
        if node is None:
            return
        self._assign_positions(node.left, level + 1)
        x = self._inorder_counter * self.h_spacing
        y = -level * self.v_spacing
        node.move_to([x, y, 0])
        self._inorder_counter += 1
        self._assign_positions(node.right, level + 1)

    def _build_edges(self, node):
        if node is None:
            return
        for child in (node.left, node.right):
            if child is not None:
                self.edges.add(Line(node.get_center(), child.get_center(), color=GREY))
        self._build_edges(node.left)
        self._build_edges(node.right)

    def _fit_to_frame(self):
        """Scale and center the tree to fit the scene."""
        if len(self.nodes) == 0:
            return
        x_coords = [n.get_center()[0] for n in self.nodes]
        width = max(x_coords) - min(x_coords) + self.h_spacing
        scale = config.frame_width * 0.9 / width
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

    def traverse_preorder(self):
        result = []

        def preorder(node):
            if node is None:
                return
            result.append(node)
            preorder(node.left)
            preorder(node.right)

        preorder(self.root)
        return result

    def traverse_postorder(self):
        result = []

        def postorder(node):
            if node is None:
                return
            postorder(node.left)
            postorder(node.right)
            result.append(node)

        postorder(self.root)
        return result


class TreeDemo(Scene):
    def construct(self):
        tree = BinaryTreeMobject(depth=2)
        self.play(Create(tree.edges))
        self.play(LaggedStart(*[GrowFromCenter(n) for n in tree.nodes], lag_ratio=0.2))
        self.wait()

        # Highlight inorder traversal
        for node in tree.traverse_inorder():
            self.play(node.highlight(), run_time=0.3)
            self.play(node.reset(), run_time=0.3)

        # Highlight leaves
        leaves = tree.get_leaves()
        self.play(*[leaf.highlight(GREEN) for leaf in leaves])
        self.wait(1)
