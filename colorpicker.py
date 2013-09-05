#!/usr/bin/env python

import gtk

window = gtk.Window()
window.add(gtk.ColorSelection())
window.show_all()

gtk.main()
