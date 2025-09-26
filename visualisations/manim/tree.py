from manim import *


class BinaryTree(Scene):
    def construct(self):
        # Parameters
        depth = 3
        node_radius = 0.35
        h_spacing = 0.4
        v_spacing = 1.5
        node_color = BLUE
        edge_color = GREY
        label_scale = 0.5

        # Build a full binary tree structure and assign integer ids
        nodes = []  # list of dicts: {id, level, left, right}

        def build(level):
            if level > depth:
                return None
            node_id = len(nodes)
            nodes.append({"id": node_id, "level": level, "left": None, "right": None})
            left = build(level + 1)
            nodes[node_id]["left"] = left
            right = build(level + 1)
            nodes[node_id]["right"] = right
            return node_id

        root_id = build(0)

        # In-order traversal to assign x indices (so layout looks balanced)
        x_counter = {"val": 0}
        x_index = {}

        def inorder(node_id):
            if node_id is None:
                return
            inorder(nodes[node_id]["left"])
            x_index[node_id] = x_counter["val"]
            x_counter["val"] += 1
            inorder(nodes[node_id]["right"])

        inorder(root_id)
        total_leaves = max(x_index.values()) + 1 if x_index else 0

        # Compute positions for each node
        positions = {}
        for n in nodes:
            nid = n["id"]
            level = n["level"]
            x = (x_index[nid] - (total_leaves - 1) / 2) * h_spacing
            y = -level * v_spacing
            positions[nid] = np.array([x, y, 0.0])

        # Create Manim objects (nodes and edges)
        node_mobs = {}
        edges = VGroup()
        for n in nodes:
            nid = n["id"]
            circ = Circle(radius=node_radius)
            circ.set_fill(node_color, opacity=1.0)
            circ.set_stroke(BLACK, width=2)
            label = Tex(str(nid + 1)).scale(label_scale)
            node_group = VGroup(circ, label).move_to(positions[nid])
            node_mobs[nid] = node_group

            # edges to children
            for child_key in ("left", "right"):
                child = n[child_key]
                if child is not None:
                    start = positions[nid] + DOWN * node_radius * 0.9
                    end = positions[child] + UP * node_radius * 0.9
                    edge = Line(start, end, color=edge_color)
                    edges.add(edge)

        all_nodes = VGroup(*[node_mobs[n["id"]] for n in nodes])

        # Animate edges first, then nodes
        self.play(Create(edges), run_time=1.2)
        self.play(LaggedStart(*[GrowFromCenter(node) for node in all_nodes], lag_ratio=0.06))
        self.wait(0.6)

        # Highlight root
        root = node_mobs[root_id]
        self.play(root.animate.scale(1.1), run_time=0.4)
        self.play(root.animate.scale(1 / 1.1), run_time=0.25)

        # Highlight leaves
        leaves = [n for n in nodes if n["left"] is None and n["right"] is None]
        leaves_mobs = VGroup(*[node_mobs[n["id"]] for n in leaves])
        self.play(
            LaggedStart(
                *[leaf.animate.set_fill(GREEN, opacity=1.0) for leaf in leaves_mobs], lag_ratio=0.08
            )
        )
        self.wait(1)

        self.play(FadeOut(edges), FadeOut(all_nodes))
