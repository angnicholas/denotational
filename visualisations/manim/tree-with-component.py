from manim import *


class LabeledNode(VGroup):
    def __init__(self, label, radius=0.35, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius).set_fill(color, 1).set_stroke(BLACK, 2)
        self.text = Text(str(label)).scale(0.4)
        self.add(self.circle, self.text)
        self.label = label

    def highlight(self, color=YELLOW):
        return self.circle.animate.set_fill(color)

    def reset(self, color=BLUE):
        return self.circle.animate.set_fill(color)


class BinaryTreeMobject(VGroup):
    def __init__(self, depth=3, h_spacing=1.2, v_spacing=1.5, **kwargs):
        super().__init__(**kwargs)
        self.nodes = {}  # id -> LabeledNode
        self.edges = VGroup()
        self.depth = depth
        self.h_spacing, self.v_spacing = h_spacing, v_spacing

        # Build full binary tree structure
        self.root_id = self._build_tree(0)
        self.add(self.edges, *self.nodes.values())
        self._relayout()

    def _build_tree(self, level, next_id=[0]):
        if level > self.depth:
            return None
        node_id = next_id[0]
        next_id[0] += 1
        node = LabeledNode(node_id + 1)
        self.nodes[node_id] = node
        # Recursively build children and store actual node objects
        left = self._build_tree(level + 1, next_id)
        right = self._build_tree(level + 1, next_id)
        node.left = self.nodes[left] if left is not None else None
        node.right = self.nodes[right] if right is not None else None
        return node_id

    def _relayout(self):
        """Position nodes and update edges."""
        # Assign x by inorder index
        x_index = {}
        counter = [0]

        def inorder(nid):
            if nid is None:
                return
            inorder(self.nodes[nid].left)
            x_index[nid] = counter[0]
            counter[0] += 1
            inorder(self.nodes[nid].right)

        inorder(self.root_id)
        total = max(x_index.values()) + 1

        # Positions
        positions = {}
        for nid, node in self.nodes.items():
            level = self._get_level(nid)
            x = (x_index[nid] - (total - 1) / 2) * self.h_spacing
            y = -level * self.v_spacing
            node.move_to([x, y, 0])
            positions[nid] = node.get_center()

        # Update edges
        self.edges.become(VGroup())  # ✅ reset
        for nid, node in self.nodes.items():
            for child in (node.left, node.right):
                if child is not None:
                    start = positions[nid]
                    end = positions[child]
                    self.edges.add(Line(start, end))

    def _get_level(self, nid):
        """Compute depth by walking from root."""
        # (For full binary tree it's implicit, but we can do this cleanly)
        # Here: just count how far label grows
        return int(np.floor(np.log2(nid + 1)))

    # Public API
    def get_leaves(self):
        return [node for node in self.nodes.values() if node.left is None and node.right is None]

    def traverse_inorder(self):
        order = []

        def inorder(nid):
            if nid is None:
                return
            inorder(self.nodes[nid].left)
            order.append(self.nodes[nid])
            inorder(self.nodes[nid].right)

        inorder(self.root_id)
        return order


class TreeDemo(Scene):
    def construct(self):
        tree = BinaryTreeMobject(depth=4)
        self.play(Create(tree.edges))
        self.play(LaggedStart(*[GrowFromCenter(n) for n in tree.nodes.values()], lag_ratio=0.2))
        self.wait()

        # Highlight inorder traversal
        for node in tree.traverse_inorder():
            self.play(node.highlight(), run_time=0.3)
            self.play(node.reset(), run_time=0.3)

        # Highlight leaves
        leaves = tree.get_leaves()
        self.play(*[leaf.highlight(GREEN) for leaf in leaves])
        self.wait()
