#!/usr/bin/env python3

import i3ipc
import re
from config import OUTPUTS, WORKSPACES

i3 = i3ipc.Connection()
RULES = []
OLD_FOCUS = None

def init_rules():
	for workspace in WORKSPACES:
		name = workspace['name']
		rules = workspace['match']
		for rule in rules:
			RULES.append({'rule': re.compile(rule), 'workspace': name})

def get_current_workspace():
	workspaces = i3.get_workspaces()
	workspace = list(filter(lambda o: o.focused, workspaces))[0]
	return workspace

def get_current_output():
	return get_current_workspace().output


def ev_window_new(i3, e, *args, **kwargs):
	window_name = e.container.name
	current_output = get_current_output()
	try:
		current_output_id = OUTPUTS[current_output]
	except:
		current_output_id = 0

	for rule in RULES:
		if rule['rule'].match(window_name):
			workspace_name = f"{current_output_id}{rule['workspace']}"
			break
	else:
		workspace_name = f"{current_output_id}9: {window_name}"

	e.container.command(f"move container to workspace {workspace_name}")
	i3.command(f"workspace {workspace_name}")

def ev_window_close(i3, e, *args, **kwargs):
	global OLD_FOCUS
	workspace = i3.get_tree().find_focused().workspace()
	if workspace.leaves():
		return
	if not OLD_FOCUS:
		return

	leaves = OLD_FOCUS.leaves()
	if leaves:
		leaves[0].command(f"focus")
	else:
		OLD_FOCUS.command(f"focus")

def ev_ws_focus(i3, e, *args, **kwargs):
	global OLD_FOCUS
	if not e.old:
		return
	if e.old == OLD_FOCUS:
		return

	OLD_FOCUS = e.old

init_rules()
i3.on(i3ipc.Event.WINDOW_NEW, ev_window_new)
i3.on(i3ipc.Event.WINDOW_CLOSE, ev_window_close)
i3.on(i3ipc.Event.WORKSPACE_FOCUS, ev_ws_focus)
i3.main()
