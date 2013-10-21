import os, shutil, math, sublime, sublime_plugin, types

class VintageLinesEventListener(sublime_plugin.EventListener):
	def __init__(self):
		self.in_check_settings = False
		self.icon_count = 99
		self.on_load = self.on_new = self.on_activated

		# Set icon path depending on version
		if int(sublime.version()) >= 3000:
			self.icon_path = "Packages/VintageLines/icons/%s/%s.png"
		else:
			self.icon_path = "../VintageLines/icons/%s/%s"

	def showRelativeNumbers(self):
		view = self.view

		view.settings().set('line_numbers', False)

		cur_line = view.rowcol(view.sel()[0].begin())[0]
		start_line = max(cur_line-self.icon_count, 0)
		end_line = min(cur_line+self.icon_count, self.view.rowcol(self.view.size())[0])

		lines = self.view.lines(sublime.Region(self.view.text_point(start_line, 0), self.view.text_point(end_line + 1, 0)))

		# Append the last line's region manually (if necessary)
		if (len(lines) < end_line - start_line + 1):
			last_text_point = lines[-1].end() + 1
			lines.append(sublime.Region(last_text_point, last_text_point))

		for i in range(start_line, start_line + len(lines)):
			name = 'linenum' + str(i-start_line)
			icon = str(int(math.fabs(cur_line - i)))

			view.add_regions(name, [lines[i-start_line]], 'linenums', self.icon_path % (sublime.platform(), icon), sublime.HIDDEN)

	def removeRelativeNumbers(self):
		self.view.settings().set('line_numbers', True)
		# Remove all relative line number regions within viewport
		for i in range(2*self.icon_count+1):
			if self.view.get_regions('linenum' + str(i)):
				self.view.erase_regions('linenum' + str(i))

	def checkSettings(self):
		cur_line = self.view.rowcol(self.view.sel()[0].begin())[0]

		if cur_line == None:
			settings.set("vintage_lines.force_mode", True);

		if self.in_check_settings:
			# As this function is called when a setting changes, and its children also
			# changes settings, we don't want it to end up in an infinite loop.
			return

		self.in_check_settings = True

		if self.view:
			settings = self.view.settings()

			if settings.has("vintage_lines.force_mode"):
				show = settings.get("vintage_lines.force_mode")
			elif type(settings.get('command_mode')) is bool:
				show = settings.get('command_mode')
			else:
				show = False

			mode = settings.get('vintage_lines.mode', False)
			line = settings.get('vintage_lines.line', -1)
			lines = settings.get('vintage_lines.lines', -1)

			update = mode != show
			update = update or line != self.view.rowcol(self.view.sel()[0].begin())[0]
			update = update or lines != self.view.rowcol(self.view.size())[0]
			if update:
				if show:
					self.removeRelativeNumbers()
					self.showRelativeNumbers()
				else:
					self.removeRelativeNumbers()

				self.view.settings().set('vintage_lines.line', self.view.rowcol(self.view.sel()[0].begin())[0])
				self.view.settings().set('vintage_lines.mode', show)
				self.view.settings().set('vintage_lines.lines', self.view.rowcol(self.view.size())[0])

		self.in_check_settings = False

	def on_activated(self, view):
		self.view = view
		if view:
			view.settings().clear_on_change("VintageLines")
			view.settings().set('vintage_lines.line', -1) # Just to force an update on activation
			view.settings().add_on_change("VintageLines", self.checkSettings)
		self.checkSettings()

	def on_selection_modified(self, view):
		sublime.set_timeout(self.checkSettings, 10)

