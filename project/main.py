#
# Calls the necessary modules in order.
# Provides user options for specific analyses.
#

import data_extraction
import build_gui
from build_gui import Tk

runList         = []
window          = Tk()

frame_1     = build_gui.buildFrame(window)
frame_2     = build_gui.buildFrame(window)

frame_1.pack(fill="both", expand=True)

build_gui.frameFill_START(frame_1, runList)
build_gui.states.append(frame_1)

build_gui.frameFill_PRIMARY(frame_2, runList)
build_gui.states.append(frame_2)

#loop window
window.geometry("800x600")
window.configure(bg = "#FFFFFF")
window.mainloop()

print(runList)