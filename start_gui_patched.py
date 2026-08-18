import sys

sys.path.insert(0, r"C:\kohya_ss_link")

import gradio.networking as networking

# Kohya GUI relies on Gradio's localhost self-check, which can fail under
# some proxy/network configurations even though 127.0.0.1 is reachable.
networking.url_ok = lambda url: True

import runpy

sys.argv = ["kohya_gui.py"] + sys.argv[1:]
runpy.run_path(r"C:\kohya_ss_link\kohya_gui.py", run_name="__main__")
