import os

filename = "python.pdf"
output_file = "copy_python.pdf" #destination of copied file


#Open it in rb (read binary)  mode
with open(filename, "rb") as file:
    image_data = file.read()

print("===Binary Data loaded ===")

print("Type: ",type(image_data)) # TAKE NOTE WHAT IT DOES
# [:20] -> from the start to 20th 
# [2:3] => from index 2 to index 3 not including 3
# [1:] => From index 1 to end
print("First 20 bytes: ", image_data[:20])

# bytesize = len - 45k 
print("Total byyte size: ",len(image_data))


#another example on type
print("-- example on type()--")
str ="Hello world"
print(type(str))
num = 123
print(type(num))
hungry = False
print(type(hungry))
data = b"Hello World"
print(type(data))

#Copy the bytes into new file
# wb - write as a byte
with open(output_file, "wb")  as file:
    file.write(image_data)

print(f"Binary data written to {output_file}")

# os (filesystem library)
# os.path-> get the current path of the folder
# getsize -> get the size of given file name
original_size = os.path.getsize(filename)
copied_size = os.path.getsize(output_file)

print("\n === File Size Validation ===")
print("Original File Size:",original_size, "bytes")
print("Copied file size", copied_size,"bytes")

if original_size == copied_size:
    print("Validation passed: file sized matches")
else:
    print("Validation failed, file size doe not matched")