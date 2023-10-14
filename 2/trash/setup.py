from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

#packages = ["idna","PySide6","time","networkx","math"]
packages = ["idna","PySide6","time","networkx","math"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "name",
    options = options,
    version = "1",
    description = 'any description',
    executables = executables
)

