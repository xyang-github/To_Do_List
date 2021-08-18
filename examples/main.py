from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class CustomTouchMixin(object):

    def __init__(self, *args, **kwargs):
        super(CustomTouchMixin, self).__init__(*args, **kwargs)
        self.register_event_type("on_really_touch_down")

    def on_really_touch_down(self, touch):
        pass


class CustomTouchWidgetMixin(CustomTouchMixin):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch("on_really_touch_down", touch)
        return super(CustomTouchWidgetMixin, self).on_touch_down(touch)


class CustomTouchLayoutMixin(CustomTouchMixin):

    def on_touch_down(self, touch):
        for child in self.walk():
            if child is self: continue
            if child.collide_point(*touch.pos):
                # let the touch propagate to children
                return super(CustomTouchLayoutMixin, self).on_touch_down(touch)
        else:
            super(CustomTouchLayoutMixin, self).dispatch("on_really_touch_down", touch)
            return True


class TouchHandlerBoxLayout(CustomTouchLayoutMixin, BoxLayout):
    pass


class TouchAwareButton(CustomTouchWidgetMixin, Button):
    pass


class TestApp(App):

    def on_background_touch(self):
        print("Background Touched")

    def on_button_touch(self, button_text):
        print("'{}' Touched".format(button_text))


if __name__ == "__main__":
    TestApp().run()
