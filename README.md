# GPS_UserInterface
GUI for GPS simulators.

To Do:
1. Create save button/option
2. Write to JSON file.
3. Load different configuration in same JSON file.
4. Create way to select different option.
	- drop down?
5. Control tree order from buttons in bottom frame
6. changed order of commands using buttons on TabTreeMouseOver buttons
7. Change order of Tabs.
8. Rename Tabs
9. File Open to select another JSON.
10. Allow only one one of each window to open.
11. Scaling and resolution on diffent monitors.


Lower Priority:
- Implement WOL option.

- Simplify ClientTabFrame class as it sloppy.
	- ScrollFrame should only worry about packing ClientTabFrame.
	- ClientTabFrame will handle packing TabBarTree and TabTreeMouseOver into itself.

- Refactor Configuration Class. Create new classes for each frame.

Eventually:
- Lightmode/Darkmode.
- Output window
- Give use ability to change color of each tab tree for visual grouping.



