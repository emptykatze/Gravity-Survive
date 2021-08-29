# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 05:01:45 2021

@author: USUARIO
"""

#import cx_Freeze

#executables=[cx_Freeze.Executable("principal.py", icon="icon.png",shortcut_name="Gravity Survive",shortcut_dir="DesktopFolder")]

#cx_Freeze.setup(name="Gravity Survive", options={"build_exe":{"packages":["pygame"],"include_files":["imagenes","librerias","sonidos"]}}, executables=executables)
import cx_Freeze

executables = [cx_Freeze.Executable("GravitySurvive.py",
                                   shortcut_name="Gravity Survive",
                                   icon = "icon.ico",
                                   base = "Win32GUI",
                                   shortcutDir=("DesktopFolder"))]

build_exe_options = {"packages": ["pygame","numpy"],
                     "include_files":["imagenes",
                                      "librerias",
                                      "sonidos",
                                      "icon.ico"]}

cx_Freeze.setup(
    name = "Gravity Survive",
    version = "1.0",
    shortcutDir=("DesktopFolder"),
    icon="icon.ico",
    description = "Gravity Survive",
    options = {"build_exe": build_exe_options},
    executables = executables
    )