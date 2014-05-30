from cx_Freeze import setup, Executable

exe=Executable(
     script="randstudent3.py",
     base="Win32Gui",
     icon="image\start.ico"
     )
includefiles=["image\smile.png","image\sysmenu.png", "image\cry.png", "student.db", "msvcr100.dll", "MSVCP100.dll"]
includes=[]
excludes=[]
packages=[]
setup(
     version = "1.0",
     description = "课堂随机提问",
     author = "iefan",
     name = "课堂随机提问",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )