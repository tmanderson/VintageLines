import math, threading, sublime, sublime_plugin

class VintageLinesCommand(sublime_plugin.WindowCommand):
	def run(self, modified = False):
		window = self.window

		# Quick fix, view.clear_on_change was killing sublime, had to resort
		# to set_timeout
		if not hasattr(window, 't') and not modified:
			window.t = sublime.set_timeout(self.checkSettings, 200)

		group = window.active_group()
		self.view = window.active_view_in_group(group)
		
		self.lastVal = self.view.settings().get('command_mode')

		if modified:
			self.removeRelatveLneNumbers()
			self.checkCommand()

	def checkSettings(self):
		if self.view.settings().get('command_mode') != self.lastVal:
			self.checkCommand()

		self.window.t = sublime.set_timeout(self.checkSettings, 200)

	def checkCommand(self):
		in_command = self.view.settings().get('command_mode')
		
		if in_command:
			self.renderRelativeLineNumbers()
		else:
			self.removeRelatveLneNumbers()
			self.bols = []

		self.lastVal = in_command

	def renderRelativeLineNumbers(self):
		self.rendered = True

		view = self.view

		cur_line = view.rowcol(view.sel()[0].begin())[0] - view.rowcol(view.visible_region().begin())[0]

		lines = self.view.lines(view.visible_region())

		for i in range(len(lines)):
			name = 'linenum' + str(i)
			icon = str(int(math.fabs(cur_line - i)))
			
			view.add_regions(name, [lines[i]], 'linenums', icon, sublime.HIDDEN)

	def removeRelatveLneNumbers(self):

		regs = self.view.find_all('^\d+\t\t')

		for i in range(100):
			if self.view.get_regions('linenum' + str(i)):
				self.view.erase_regions('linenum' + str(i))

	def moveCursor(direction):
		self.view.window().run_command('move', {"by": "lines", "forward": True})

class modeListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		view.window().run_command('vintage_lines')

	def on_modified(self, view):
		view.window().run_command('vintage_lines', {"modified": True})