from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
print("Place card...")
id, text = reader.read()
print("ID:", id)
print("Text:", text)
