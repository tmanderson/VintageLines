import math, sublime, sublime_plugin

class VintageLinesCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = self.window
		# Get the status of the current view, to see what
		# mode we are in

		group = window.active_group()
		view = window.active_view_in_group(group)

		lines = view.lines(view.visible_region())

		# icon = 'data:image/png;base64,' + open('/Users/mitchellanderson/Library/Application Support/Sublime Text 2/Packages/VintageLines/icons/circle.png').read().encode("base64").replace("\n", "")

		self.renderRelativeLineNumbers(view)

	def renderRelativeLineNumbers(self, view):
		cur_line = view.line(view.sel()[0].begin()).begin()
		lines = view.lines(view.visible_region())

		for l in lines:
			icon = (cur_line - 1) - l.begin()
			view.add_regions('linenums' + str(icon), [l], str(math.fabs(icon)))

	def moveCursor(direction):
		self.view.window().run_command('move', {"by": "lines", "forward": True})

class ShowLineNumbers(sublime_plugin.TextCommand):
	def run(self, args):
		self.view.settings().set('line_numbers', True)
		self.view.erase_regions('line_numbers');
		self.view.run_command('exit_insert_mode')

class LineDown(sublime_plugin.TextCommand):
	def run(self, args):
		
		mode = self.view.get_status('mode')

		# Don't override the down arrow!
		self.view.window().run_command('move', {"by": "lines", "forward": True})
		# sublime.run_command('vintage_lines_command', 'moveCursor')

		if mode == 'INSERT MODE':
			self.view.settings().set('line_numbers', False);
			# Once we've moved down, get the current position
			focus_line = self.view.sel()
			self.view.add_regions('line_numbers', [focus_line[0]], 'first', '1', sublime.HIDDEN)

class LineUp(sublime_plugin.TextCommand):
	def run(self, args):

		mode = self.view.get_status('mode')
		
		# Don't override the up arrow!
		self.view.window().run_command('move', {"by": "lines", "forward": False})
		# sublime.run_command('vintage_lines_command', 'moveCursor')

		if mode == 'INSERT MODE':
			# Once we've moved down, get the current position
			focus_line = self.view.sel()
			self.view.add_regions('line_numbers', [focus_line[0]], 'first', '1', sublime.HIDDEN)