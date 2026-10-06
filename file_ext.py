import os
import glob

path = 'images'
file_name = 'cro'

# Use the glob module to find the file by its name
file_path = glob.glob(os.path.join(path, file_name+'*'))[0]

# Get the extension by splitting the file path by '.' and getting the last element
file_extension = file_path.split('.')[-1]

print(file_extension)

full_name = f"{file_name}.{file_extension}"
print(full_name)