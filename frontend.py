import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, Gdk, Pango, GLib

class CustomShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="C-QUENCE: A CUSTOM SHELL")
        self.set_default_size(800, 400)
        self.bg_color = Gdk.RGBA(0, 0, 0, 1)
        self.fg_color = Gdk.RGBA(1, 1, 1, 1)
        self.font_style = "Monospace"
        self.font_size = 12
        self.terminal = Vte.Terminal()
        self.set_terminal_appearance()
        self.settings_button = Gtk.Button(label="Change Appearance")
        self.settings_button.connect("clicked", self.on_settings_button_clicked)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.terminal, True, True, 0)
        box.pack_start(self.settings_button, False, False, 0)
        self.add(box)
        self.start_shell()

    def set_terminal_appearance(self):
        """ Set the terminal appearance based on saved settings. """
        self.terminal.set_colors(self.fg_color, self.bg_color)
        font_desc = Pango.FontDescription(f"{self.font_style} {self.font_size}")
        self.terminal.set_font(font_desc)

    def start_shell(self):
        shell_path = "./a.out"
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            [shell_path],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,                          
            -1,  
            None,
            None
        )

    def on_settings_button_clicked(self, button):
        settings_dialog = Gtk.Dialog("Change Appearance", self, 0, ("Cancel", Gtk.ResponseType.CANCEL, "Apply", Gtk.ResponseType.OK))
        color_button_bg = Gtk.ColorButton()
        color_button_fg = Gtk.ColorButton()
        color_button_bg.set_rgba(self.bg_color)
        color_button_fg.set_rgba(self.fg_color)
        font_style_combobox = Gtk.ComboBoxText()
        font_styles = ["Monospace", "Arial", "Courier", "Times New Roman", "Ubuntu", "DejaVu Sans Mono"]
        for style in font_styles:
            font_style_combobox.append_text(style)
        font_style_combobox.set_active(font_styles.index(self.font_style))
        font_size_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        font_size_scale.set_range(8, 30)
        font_size_scale.set_increments(1, 1)
        font_size_scale.set_value(self.font_size)
        box = settings_dialog.get_content_area()
        box.add(Gtk.Label("Choose Background Color:"))
        box.add(color_button_bg)
        box.add(Gtk.Label("Choose Text Color:"))
        box.add(color_button_fg)
        box.add(Gtk.Label("Font Style:"))
        box.add(font_style_combobox)
        box.add(Gtk.Label("Font Size:"))
        box.add(font_size_scale)
        settings_dialog.show_all()
        response = settings_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.bg_color = color_button_bg.get_rgba()
            self.fg_color = color_button_fg.get_rgba()
            self.terminal.set_colors(self.fg_color, self.bg_color)
            self.font_style = font_style_combobox.get_active_text()
            self.font_size = int(font_size_scale.get_value())

            font_desc = Pango.FontDescription(f"{self.font_style} {self.font_size}")
            self.terminal.set_font(font_desc)
        settings_dialog.destroy()

if __name__ == "__main__":
    win = CustomShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
