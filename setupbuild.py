from cx_Freeze import setup, Executable

exe=Executable(
     script="randstudent.py",
     base="Win32Gui",
     icon="image\start.ico"
     )
includefiles=["image\ex_stu.png","image\smile.png", "image\cry.png"]
includes=[]
excludes=[]
packages=[]
setup(

     version = "0.0",
     description = "No Description",
     author = "Name",
     name = "App name",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )