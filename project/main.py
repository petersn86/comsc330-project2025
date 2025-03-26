import data_extraction
import build_gui
from build_gui import Tk

window_start    = Tk()
frame_1         = build_gui.buildFrame(window_start)

window_start.geometry("800x600")
window_start.configure(bg="#FFFFFF")
window_start.resizable(False, False)
frame_1.pack(fill="both", expand=True)
build_gui.frameFill_START(frame_1)

window_start.mainloop()

window_main     = Tk()
frame_2         = build_gui.buildFrame(window_main)

window_main.geometry("800x600")
window_main.configure(bg="#FFFFFF")
window_main.resizable(False, False)
frame_2.pack(fill="both", expand=True)
build_gui.frameFill_PRIMARY(frame_2)

window_main.mainloop()

print(build_gui.runList)
print(build_gui.folderPath)
