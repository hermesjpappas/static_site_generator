import os
from copyfiles import copy_files

def main():
  # get the absolute path
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # change the working directory to the project's root directory
  project_root = os.path.join(script_dir, '..')
  os.chdir(project_root)

  copy_files("static", "public")

main()