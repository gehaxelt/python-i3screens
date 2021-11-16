i3screens
====================
A helper tool for managing i3wm workspaces on multiple monitors.

# Use-case
You have a multi-monitor setup and want to have the "same" workspaces on multiple monitors at the same time. `i3screens` is a simple python script which listens to several i3wm-events and creates the configured workspaces on the currently focused monitor. It also allows you to apply matching rules so that new windows are automatically moved to the correct workspace.


# Installation

## Dependencies
Install the `i3ipc` python package. On most systems you should be able to use `pip install i3ipc`.

## Clone the repository
Clone the repository somewhere into your home directory: `git clone https://github.com/gehaxelt/python-i3screens ~/i3screens`

## Configuration
Create the configuration file `config.py` in `~/i3screens/`. You can use `config.py.sample` as a template. 

Make sure that the `OUTPUTS` are enumerated starting at `0`. The regular expressions in `WORKSPACES` should be python `re` module compatible.

## Systemd autostart
The tool has to run in order to work. The easiest way to have it started and ran in the background is systemd. A `i3screens.service` file is included in the repo. Set it up as a user-systemd file as follows:

```
mkdir -p ~/.config/systemd/user/
cp ~/i3screens/i3screens.service ~/.config/systemd/user/
```

Now you have to edit `~/.config/systemd/user/i3screens.service` and replace `/home/YOURUSERNAME/i3screens/i3screens.py` with the path to your `i3screens.py`.

Finally, reload the systemd-daemon, enable and start the service:

```
systemctl --user daemon-reload
systemctl --user enable i3screens
systemctl --user start i3screens
```

