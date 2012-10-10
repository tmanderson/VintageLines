import os, shutil, math, sublime, sublime_plugin

class VintageLinesCommand(sublime_plugin.TextCommand):
	def run(self, args, show):

		if show == True:
			self.removeRelativeNumbers()
			self.showRelativeNumbers()
		else:
			self.removeRelativeNumbers()

	def showRelativeNumbers(self):
		view = self.view

		view.settings().set('line_numbers', False)

		cur_line = view.rowcol(view.sel()[0].begin())[0] - view.rowcol(view.visible_region().begin())[0]

		lines = self.view.lines(view.visible_region())
		icon_count = 99

		for i in range(max(cur_line-icon_count, 0), min(cur_line+icon_count+1, len(lines))):
			name = 'linenum' + str(i)
			icon = str(int(math.fabs(cur_line - i)))

			view.add_regions(name, [lines[i]], 'linenums', "../VintageLines/icons/%s/%s" % (sublime.platform(), icon), sublime.HIDDEN)

	def removeRelativeNumbers(self):
		self.view.settings().set('line_numbers', True)

		# Remove all relative line number regions within viewport
		for i in range(len(self.view.visible_region())):
			if self.view.get_regions('linenum' + str(i)):
				self.view.erase_regions('linenum' + str(i))

class VintageLinesListener(sublime_plugin.ApplicationCommand):
	def run(self):
		self.checkSettings()

	def checkSettings(self):
		window = sublime.active_window()

		if window:
			view = window.active_view_in_group(window.active_group())

			if view:
				settings 	= view.settings()

				if settings.get('command_mode'):
					view.run_command('vintage_lines', {"show":True})
				else:
					view.run_command('vintage_lines', {"show":False})

		sublime.set_timeout(self.checkSettings, 100)

def run_vintage_lines():
	sublime.run_command('vintage_lines_listener')

sublime.set_timeout(run_vintage_lines, 500)
