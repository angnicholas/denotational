from manim import *


class LabeledNode(VGroup):
    def __init__(self, label, radius=0.35, color=BLUE):
        super().__init__()
        self.circle = Circle(radius=radius).set_fill(color, 1).set_stroke(BLACK, 2)
        self.text = Text(str(label)).scale(0.5)
        self.add(self.circle, self.text)
        self.label = label
        self.left = None
        self.right = None
        self.pos = np.array([0, 0, 0])  # will store computed position

    def highlight(self, color=YELLOW):
        return self.circle.animate.set_fill(color)

    def reset(self, color=BLUE):
        return self.circle.animate.set_fill(color)


class BinaryTreeMobject(VGroup):
    def __init__(self, depth=3, node_color=BLUE, h_spacing=1.5, v_spacing=1.5):
        super().__init__()
        self.depth = depth
        self.node_color = node_color
        self.h_spacing = h_spacing
        self.v_spacing = v_spacing
        self.edges = VGroup()
        self.nodes = []

        # Build tree nodes
        self.root = self._build_tree(depth)
        # Compute positions
        self._compute_positions(self.root, 0, 0)
        # Create edges
        self._create_edges(self.root)
        # Add nodes and edges
        self.add(self.edges, *self.nodes)
        # Scale to fit frame
        self._fit_to_frame()

    def _build_tree(self, level):
        if level < 0:
            return None
        node = LabeledNode(len(self.nodes) + 1, color=self.node_color)
        self.nodes.append(node)
        node.left = self._build_tree(level - 1)
        node.right = self._build_tree(level - 1)
        return node

    def _compute_positions(self, node, x_min, x_max):
        """Recursively compute positions of each node in the tree."""
        if node is None:
            return []
        # If leaf
        if node.left is None and node.right is None:
            x = (x_min + x_max) / 2
            y = 0
            node.pos = np.array([x, y, 0])
            return [x]
        # Compute positions of children
        left_xs = self._compute_positions(node.left, x_min, (x_min + x_max) / 2)
        right_xs = self._compute_positions(node.right, (x_min + x_max) / 2, x_max)
        # Node x = midpoint of children
        all_xs = left_xs + right_xs
        node_x = sum(all_xs) / len(all_xs) if all_xs else (x_min + x_max) / 2
        node_y = -self.v_spacing * (self.depth - len(all_xs) // 2)  # y depends on depth
        node.pos = np.array([node_x, node_y, 0])
        return all_xs if all_xs else [node_x]

    def _create_edges(self, node):
        if node is None:
            return
        for child in (node.left, node.right):
            if child is not None:
                self.edges.add(Line(node.pos, child.pos, color=GREY))
                self._create_edges(child)

    def _fit_to_frame(self):
        """Scale and center tree."""
        if not self.nodes:
            return
        xs = [n.pos[0] for n in self.nodes]
        width = max(xs) - min(xs) + self.h_spacing
        scale = config.frame_width * 0.9 / width
        self.scale(scale)
        # Center
        self.move_to(ORIGIN)

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
