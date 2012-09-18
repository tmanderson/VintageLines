import os, shutil, math, sublime, sublime_plugin

# Checking to see if we've copied the icons over on load
if not os.path.exists(sublime.packages_path() + '/Theme - Default/1.png'):
	for i in range(80):
		src = sublime.packages_path() + '/VintageLines/icons/' + str(i) + '.png'
		dest = sublime.packages_path() + '/Theme - Default/' + str(i) + '.png'

		shutil.copy(src, dest)

class VintageLinesCommand(sublime_plugin.TextCommand):
	def run(self, args, show, move_forward=None):
		
		if move_forward == True:
			self.view.run_command('move', {"by":"lines","forward":True})
		elif move_forward == False:
			self.view.run_command('move', {"by":"lines","forward":False})

		if show == True:
			self.showRelativeNumbers()
		else:
			self.hideRelativeNumbers()

	def showRelativeNumbers(self):
		view = self.view

		view.settings().set('line_numbers', False)

		cur_line = view.rowcol(view.sel()[0].begin())[0] - view.rowcol(view.visible_region().begin())[0]

		lines = self.view.lines(view.visible_region())

		for i in range(len(lines)):
			name = 'linenum' + str(i)
			icon = str(int(math.fabs(cur_line - i)))
			
			view.add_regions(name, [lines[i]], 'linenums', icon, sublime.HIDDEN)

	def hideRelativeNumbers(self):
		self.view.settings().set('line_numbers', True)

		for i in range(100):
			if self.view.get_regions('linenum' + str(i)):
				self.view.erase_regions('linenum' + str(i))

class SettingsListener(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view_in_group(self.window.active_group())
		
		if view.settings().get('command_mode') == None:
			view.settings().set('command_mode', False)

		self.mode = view.settings().get('command_mode')

		self.checkSettings()

	def checkSettings(self):
		view 		= self.window.active_view_in_group(self.window.active_group())
		settings 	= view.settings();

		if settings.get('command_mode') != self.mode:
			
			self.mode = settings.get('command_mode')

			if settings.get('command_mode'):
				view.run_command('vintage_lines', {"show":True})
			else:
				view.run_command('vintage_lines', {"show":False})

		sublime.set_timeout(self.checkSettings, 200)

class modeListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		view.window().run_command('settings_listener')

	def on_selection_modified(self, view):
		show = False

		if view.settings().get('command_mode'):
			show = True

		view.run_command('vintage_lines', {"show": show})