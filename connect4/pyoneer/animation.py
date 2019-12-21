from . import interpolation


class AnimationService:

    def __init__(self):

        self.animations = []

    def add_animation(self, animation):

        self.animations.append(animation)

    def update(self, delta):

        self.animations = [animation for animation in self.animations if animation.alive]
        for animation in self.animations:
            animation.update(delta)


class Animation:

    def __init__(self, start_pos, end_pos, duration, interpolator: interpolation.Interpolator, callback):

        self.start_pos = start_pos
        self.pos = start_pos
        self.end_pos = end_pos

        self.t = 0              # Current time step in milliseconds
        # If animation duration isn't specified, calculate
        if duration is None:
            self.end_t = interpolator.compute_duration(start_pos, end_pos)

        # Otherwise, calculate the coefficients needed to complete animation in time
        else:
            self.end_t = duration   # End time step in milliseconds - can be "None"
            interpolator.compute_coefficients(duration)

        self.interpolator = interpolator
        self.callback = callback
        self.alive = True

    def update(self, delta):

        self.t += delta

        if self.t >= self.end_t:
            self.end()

        else:
            self.interpolator.interpolate(self, delta)

    def end(self):

        self.alive = False
        self.pos = self.end_pos
        self.callback()
