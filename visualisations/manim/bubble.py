from manim import *


class BubbleSort(Scene):
    def construct(self):
        # Data to sort
        data = [5, 3, 8, 1, 4]

        # Create boxes with numbers
        boxes = VGroup(
            *[
                VGroup(Square(side_length=1, color=WHITE), Text(str(num), font_size=36)).arrange(
                    DOWN, buff=0.1
                )
                for num in data
            ]
        ).arrange(RIGHT, buff=0.5)

        self.play(FadeIn(boxes))
        self.wait(1)

        # Bubble sort animation
        n = len(data)
        for i in range(n):
            for j in range(n - i - 1):
                # Highlight the pair being compared
                self.play(
                    boxes[j][0].animate.set_color(YELLOW),
                    boxes[j + 1][0].animate.set_color(YELLOW),
                    run_time=0.5,
                )

                if data[j] > data[j + 1]:
                    # Swap in data
                    data[j], data[j + 1] = data[j + 1], data[j]

                    # Swap animation
                    self.play(
                        boxes[j].animate.shift(RIGHT * 1.5),
                        boxes[j + 1].animate.shift(LEFT * 1.5),
                        run_time=0.8,
                    )
                    boxes[j], boxes[j + 1] = boxes[j + 1], boxes[j]

                # Reset colors
                self.play(
                    boxes[j][0].animate.set_color(WHITE),
                    boxes[j + 1][0].animate.set_color(WHITE),
                    run_time=0.3,
                )

        # Final highlight
        self.play(*[box[0].animate.set_color(GREEN) for box in boxes])
        self.wait(2)
