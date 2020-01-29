# import socket
# import json
import threading

import pyglet

window = pyglet.window.Window(width=1600, height=900)
# window.set_exclusive_mouse(True)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("127.0.0.1", 12345))


class TextBox(Control):

    DISABLE_NEWLINE = True

    def __init__(self, text='Yoooooo~', color=Colors.green, font_name='AncientPix', *args, **kwargs):
        Control.__init__(self, can_focus=True, *args, **kwargs)
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), dict(
            color=(0, 0, 0, 255),
            font_name=font_name,
            font_size=9,
        ))
        self.color = color
        width = self.width
        f = self.document.get_font()
        font_height = f.ascent - f.descent
        if self.height == 0:
            height = font_height
            self.height = height
        else:
            height = self.height

        l = self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width-9, font_height, multiline=False,
        )
        l.anchor_x, l.anchor_y = 'left', 'center'
        l.x, l.y = 4, height // 2 + 1
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.set_handlers(self.caret)
        self.push_handlers(self)
        from client.ui.base.baseclasses import main_window
        self.window = main_window
        self.text_cursor = self.window.get_system_mouse_cursor('text')
        self.on_lostfocus()

    def _gettext(self):
        return self.document.text

    def _settext(self, text):
        self.document.text = text

    text = property(_gettext, _settext)



    def draw(self):

        w, h = self.width, self.height

        border = [i/255.0 for i in self.color.heavy]

        fill = [i/255.0 for i in self.color.light]

        glColor3f(*fill)

        glRectf(0, 0, w, h)

        glColor3f(*border)

        glRectf(0, h, w, 0)

        self.layout.draw()



    def on_focus(self):

        self.caret.visible = True

        self.caret.mark = 0

        self.caret.position = len(self.document.text)

        self.focused = True



    def on_lostfocus(self):

        self.caret.visible = False

        self.caret.mark = self.caret.position = 0

        self.focused = False



    def on_mouse_enter(self, x, y):

        self.window.set_mouse_cursor(self.text_cursor)



    def on_mouse_leave(self, x, y):

        self.window.set_mouse_cursor(None)



    def on_mouse_drag(self, x, y, dx, dy, btn, modifier):

        # If I'm not focused, don't select texts

        if btn == mouse.LEFT and self.focused:

            x = max(4, x)

            self.caret.on_mouse_drag(x, y, dx, dy, btn, modifier)

        return pyglet.event.EVENT_HANDLED



    def on_mouse_press(self, x, y, btn, modifier):

        self.set_capture('on_mouse_release', 'on_mouse_drag')



    def on_mouse_release(self, x, y, btn, modifier):

        self.release_capture('on_mouse_release', 'on_mouse_drag')

        return True



    def on_key_press(self, symbol, modifiers):

        if modifiers & KEYMOD_MASK == key.MOD_CTRL:

            if symbol == key.A:

                self.caret.position = 0

                self.caret.mark = len(self.text)

                return pyglet.event.EVENT_HANDLED



            elif symbol == key.C:

                start = self.layout.selection_start

                end = self.layout.selection_end

                if start != end:

                    pyperclip.copy(self.text[start:end])

                return pyglet.event.EVENT_HANDLED



            elif symbol == key.ENTER:

                if self.DISABLE_NEWLINE: return

                self.dispatch_event('on_text', u'\n')

                return pyglet.event.EVENT_HANDLED



            elif symbol == key.V:

                content = unicode(pyperclip.paste())

                if self.DISABLE_NEWLINE:

                    for le in (u'\r\n', u'\r', u'\n'):

                        content = content.replace(le, u' ')

                self.dispatch_event('on_text', content)

                return pyglet.event.EVENT_HANDLED



            elif symbol == key.X:

                start = self.layout.selection_start

                end = self.layout.selection_end
                if start != end:
                    pyperclip.copy(self.text[start:end])
                    self.dispatch_event('on_text', u'')
                return pyglet.event.EVENT_HANDLED


    def on_text(self, text):
        if text == '\r':
            self.dispatch_event('on_enter')
            return pyglet.event.EVENT_HANDLED


TextBox.register_event_type('on_enter')


def send(connection, **dictionary):
    connection.send(json.dumps(dictionary).encode())


fps_display = pyglet.window.FPSDisplay(window)
# send(s, version=10.1)


@window.event
def on_draw():
    window.clear()
    # a = s.recv(1024).decode()
    # b = json.loads(a)

    label = pyglet.text.Label(str(pyglet.clock.get_fps()),
                              font_name='Times New Roman',
                              font_size=20,
                              x=window.width // 2, y=window.height // 2,
                              anchor_x='center', anchor_y='center')
    label.draw()
    fps_display.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    pass


@window.event
def on_mouse_motion(x, y, dx, dy):
    pass


pyglet.app.run()
