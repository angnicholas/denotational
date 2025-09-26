from manim import *


class LabeledNode(VGroup):
    def __init__(self, label, radius=0.35, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius).set_fill(color, 1).set_stroke(BLACK, 2)
        self.text = Text(str(label)).scale(0.5)
        self.add(self.circle, self.text)
        self.label = label
        self.left = None  # child nodes
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

        self.nodes = {}  # id -> LabeledNode
        self.edges = VGroup()

        # Build tree structure
        self.root_id = self._build_tree(0)
        self.tree_group = VGroup(self.edges, *self.nodes.values())
        self.add(self.tree_group)

        self._relayout()
        self._fit_to_frame()

    def _build_tree(self, level, next_id=[0]):
        if level > self.depth:
            return None
        node_id = next_id[0]
        next_id[0] += 1
        node = LabeledNode(node_id + 1, color=self.node_color)
        self.nodes[node_id] = node

        left_id = self._build_tree(level + 1, next_id)
        right_id = self._build_tree(level + 1, next_id)

        node.left = self.nodes[left_id] if left_id is not None else None
        node.right = self.nodes[right_id] if right_id is not None else None

        return node_id

    def _get_level(self, nid):
        """Compute level based on root distance (for full binary tree this works)."""
        level = 0
        while True:
            if nid == 0:
                break
            level += 1
            nid = (nid - 1) // 2
        return level

    def _relayout(self):
        """Compute node positions and edges."""
        # inorder traversal for x positions
        x_index = {}
        counter = [0]

        def inorder_assign(nid):
            if nid is None:
                return
            inorder_assign(self.nodes[nid].left.label - 1 if self.nodes[nid].left else None)
            x_index[nid] = counter[0]
            counter[0] += 1
            inorder_assign(self.nodes[nid].right.label - 1 if self.nodes[nid].right else None)

        inorder_assign(self.root_id)
        total = max(x_index.values()) + 1

        # Assign positions
        positions = {}
        for nid, node in self.nodes.items():
            level = self._get_level(nid)
            x = (x_index[nid] - (total - 1) / 2) * self.h_spacing
            y = -level * self.v_spacing
            node.move_to([x, y, 0])
            positions[nid] = node.get_center()

        # Build edges
        self.edges.become(VGroup())
        for nid, node in self.nodes.items():
            for child in (node.left, node.right):
                if child is not None:
                    self.edges.add(Line(node.get_center(), child.get_center(), color=GREY))

    def _fit_to_frame(self):
        """Scale and center tree to fit scene."""
        self.tree_group.scale_to_fit_width(config.frame_width * 0.9)
        self.tree_group.move_to(ORIGIN)

    # Public API
    def get_leaves(self):
        return [node for node in self.nodes.values() if node.left is None and node.right is None]

    def traverse_inorder(self):
        result = []

        def inorder(node):
            if node is None:
                return
            inorder(node.left)
            result.append(node)
            inorder(node.right)

        inorder(self.nodes[self.root_id])
        return result

    def traverse_preorder(self):
        result = []

        def preorder(node):
            if node is None:
                return
            result.append(node)
            preorder(node.left)
            preorder(node.right)

        preorder(self.nodes[self.root_id])
        return result

    def traverse_postorder(self):
        result = []

        def postorder(node):
            if node is None:
                return
            postorder(node.left)
            postorder(node.right)
            result.append(node)

        postorder(self.nodes[self.root_id])
        return result


class TreeDemo(Scene):
    def construct(self):
        tree = BinaryTreeMobject(depth=2)
        self.play(Create(tree.edges))
        self.play(LaggedStart(*[GrowFromCenter(n) for n in tree.nodes.values()], lag_ratio=0.2))
        self.wait(0.5)

        # Highlight inorder traversal
        for node in tree.traverse_inorder():
            self.play(node.highlight(), run_time=0.3)
            self.play(node.reset(), run_time=0.3)

        # Highlight leaves
        leaves = tree.get_leaves()
        self.play(*[leaf.highlight(GREEN) for leaf in leaves])
        self.wait(1)
