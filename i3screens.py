import i3ipc
import re

i3 = i3ipc.Connection()

OUTPUTS = {
	'eDP': 0,
	'DVI-I-2-2': 1,
	'DVI-I-1-1': 2
}

WORKSPACES = [
	{
		"name": "1: Shell",
		"match": [
			".*kitty.*"
		]
	},
	{
		"name": "2: Internet",
		"match": [
			".*firefox.*",
			".*opera.*"
		]
	},
	{
		"name": "3: Code",
		"match": [
			".*Geany.*",
			".*Subl.*",
			".*subl.*"
		]
	},
	{
		"name": "4: Chat",
		"match": [
			".*Signal.*",
			".*Element.*"
		]
	},
	{
		"name": "5: Mail",
		"match": [
			".*Thunderbird.*"
		]
	},
	{
		"name": "6: Office",
		"match": [
			".*LibreOffice.*",
			".*TexStudio.*"
		]
	},
	{
		"name": "7: Sonstiges",
		"match": [
			".*KeePassXC.*"
		]
	}
]

RULES = []

def init_rules():
	for workspace in WORKSPACES:
		name = workspace['name']
		rules = workspace['match']
		for rule in rules:
			RULES.append({'rule': re.compile(rule), 'workspace': name})

def get_current_workspace():
	workspaces = i3.get_workspaces()
	return list(filter(lambda o: o.focused, workspaces))[0]

def get_current_output():
	return get_current_workspace().output


def new_window(i3, e, *args, **kwargs):
	window_name = e.container.name
	current_output = get_current_output()
	try:
		current_output_id = OUTPUTS[current_output]
	except:
		current_output_id = 0

	for rule in RULES:
		if rule['rule'].match(window_name):
			workspace_name = f"{current_output_id}.{rule['workspace']}"
			break
	else:
		workspace_name = f"{current_output_id}.?: {window_name}"

	e.container.command(f"move container to workspace {workspace_name}")

init_rules()

i3.on(i3ipc.Event.WINDOW_NEW, new_window)
i3.main()