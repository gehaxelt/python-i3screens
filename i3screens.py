#!/usr/bin/env python3
# @author gehaxelt
# @repo https://github.com/gehaxelt/python-i3screens

import i3ipc
import re
from config import OUTPUTS, WORKSPACES

i3 = i3ipc.Connection()
RULES = [] # List of compiled matching rules.
PREV_WS = None # Previous workspace that was focused.

def init_rules():
	"""
	Compile the regular expressions used for matching windows to workspaces.
	"""
	for workspace in WORKSPACES:
		name = workspace['name']
		rules = workspace['match']
		for rule in rules:
			RULES.append({'rule': re.compile(rule), 'workspace': name})

def get_current_workspace():
	"""
	Identify the currently used workspace. We can use the "focused" property, since only one WS can be focused at a time (apparently?).
	"""
	workspaces = i3.get_workspaces()
	workspace = list(filter(lambda o: o.focused, workspaces))[0]
	return workspace

def get_current_output():
	"""
	Identify on which monitor the current workspace is, so that we can spawn the new workspace on the right monitor.
	"""
	return get_current_workspace().output


def ev_window_new(i3, event, *args, **kwargs):
	"""
	If a new window spawns, move it to the right workspace on the current monitor. 
	"""
	window_class = event.container.window_class
	current_output = get_current_output()
	try:
		current_output_id = OUTPUTS[current_output]
	except:
		current_output_id = 0

	for rule in RULES:
		if rule['rule'].match(window_class):
			workspace_name = f"{current_output_id}{rule['workspace']}"
			break
	else:
		workspace_name = f"{current_output_id}9: {window_class}"

	event.container.command(f"move container to workspace {workspace_name}")
	i3.command(f"workspace {workspace_name}")

def ev_window_close(i3, event, *args, **kwargs):
	"""
	Check if we just closed all windows of a workspace. If so, focus the previous workspace, thereby removing the empty workspace.
	"""
	global PREV_WS
	workspace = i3.get_tree().find_focused().workspace()
	if workspace.leaves():
		return
	if not PREV_WS:
		return

	leaves = PREV_WS.leaves()
	if leaves:
		leaves[0].command(f"focus")
	else:
		PREV_WS.command(f"focus")

def ev_ws_focus(i3, event, *args, **kwargs):
	"""
	Remember the last focused workspace, so that we can switch to it if we empty the currently focused one.
	"""
	global PREV_WS
	if not event.old:
		return
	if event.old == PREV_WS:
		return

	PREV_WS = event.old

init_rules()
i3.on(i3ipc.Event.WINDOW_NEW, ev_window_new)
i3.on(i3ipc.Event.WINDOW_CLOSE, ev_window_close)
i3.on(i3ipc.Event.WORKSPACE_FOCUS, ev_ws_focus)
i3.main()
