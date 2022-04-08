from os import path

from typing import List  # noqa: F401
from libqtile import hook
from libqtile import bar, layout, widget

from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import subprocess

mod = "mod4"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "m", lazy.spawn("rofi -show drun")),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    #Screenshots
    Key([mod], "s", lazy.spawn("screenshot")),
    Key([mod,"shift"], "s", lazy.spawn("screenshot window")),
    Key([mod, "control"], "s", lazy.spawn("screenshot select")),
]

groups = [Group(i) for i in [
    "DEV", "WWW", "SYS", "CODE", "TFM", "OBS", "STEAM", "MUS", "VID",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(),
    layout.MonadTall(
        border_width = 0,
        #border_width = None;
        #border_focus = "#01BFFE",
        border_focus = None,
        #border_normal = "#7400DE",
        border_normal = None,
        margin = 15,
        single_border_width = 0,
        single_margin = 0,
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrains Mono Nerd Font",
    fontsize = 14,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(
                    center_aligned=True,
                    fontsize=10,
                    inactive="#FFFFFF",
                    active="#80BFF7",
                    rounded=False,
                    padding_y=0,
                    padding_x=0,
                    disable_drag=True,
                    highlight_method='line',
                    urgent_alert_method='block',
                    this_current_screen_border="#FB5883",
                    other_current_screen_border="#FF6C6B",
                    other_screen_border="#DFDFDF",
                    highlight_color="#282A36",
                    foreground="#DFDFDF",
                    background="#282A36",
                ),

                widget.TextBox(
                    text='|',
                    font="JetBrainsMono Nerd Font",
                    foreground="#FFFFFF",
                    background="#282A36",
                    padding=2,
                    fontsize=18,
                ),

                widget.Prompt(),
                widget.WindowName(
                    font="JetBrains Mono Bold Nerd Font",
                    fontsize=12,
                    background="#282A36",
                    foreground="#8258FA",
                    max_chars=50,
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox(
                    text="", #nf-pl-right_hard_divider
                    padding=0,
                    fontsize=27,
                    foreground="#F7819F",
                    background="#282C34",
                ),
                widget.TextBox(
                    text='', #nf-fa-download
                    fontsize=14,
                    foreground="#000000",
                    background="#F7819F",
                    padding=4,
                ),
                widget.CheckUpdates(
                    distro='Arch',
                    font='JetBrainsMono Bold',
                    fontsize=12,
                    background="#F7819F",
                    colour_have_updates="#000000",
                    colour_no_updates="#000000",
                    no_update_string="0",
                    display_format="{updates}",
                    update_interval=1800,
                    custom_command="checkupdates",
                    padding=5,
                ),
                widget.TextBox(
                    text="", #nf-pl-right_hard_divider
                    padding=0,
                    fontsize=27,
                    foreground="#88F98F",
                    background="#F7819F",
                ),
                widget.TextBox(
                    text="", #nf-fa-feed
                    fontsize=14,
                    foreground="#000000",
                    background="#88F98F",
                    padding=4,
                ),
                widget.Net(
                    font="JetBrainsMono Bold",
                    #interface = None,
                    format='{down} ↓↑ {up}',
                    background="#88F98F",
                    fontsize=12,
                    foreground="#000000",
                ),
                widget.TextBox(
                    text="", #nf-pl-right_hard_divider
                    padding=0,
                    background="#88F98F",
                    fontsize=27,
                    foreground="#4E7CF9",
                ),
                widget.TextBox(
                    text="", #nf-mdi-calendar_clock
                    fontsize=14,
                    padding=4,
                    background="#4E7CF9",
                    foreground="#000000",
                ),
                widget.Clock(format='%Y/%m/%d - %H:%M',
                    font="JetBrainsMono Bold",
                    fontsize=12,
                    foreground="#000000",
                    background="#4E7CF9",
                    #markup = True,
                    padding=3,
                ),
                widget.TextBox(
                    text ="", #nf-pl-right_hard_divider
                    padding=0,
                    background="#4E7CF9",
                    fontsize=27,
                    foreground='#282A36',
                ),
                widget.Battery(
                    background="#282A36",
                    format='{char} {percent:2.0%}',
                    charge_char="", #nf-mdi-battery_charging
                    full_char="", #nf-mdi-battery
                    discharge_char="", #nf-mdi-battery_50
                    empty_char="", #nf-mdi-battery_outline
                    low_percentage=0.2,
                    notify_below=True,
                    foreground="#BE81F7",
                    update_interval=60,
                    fontsize=12,
                ),
                widget.PulseVolume(
                    channel="master",
                    padding=3,
                    background="#282A36",
                    emoji="", #nf-fa-volume_up
                    fontsize=14,
                    foreground="#BE81F7",
                ),
                widget.Systray(background="#282A36"),
                widget.QuickExit(
                    fontsize=10,
                    background="#282A36",
                    foreground="#BE81F7",
                ),
            ],
            20,
            background="#2F2E2F",
            opacity=1.00,
            center_aligned=True
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
