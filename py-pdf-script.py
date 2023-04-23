from typing import Dict
from PyPDF2 import PdfReader, PdfWriter

# Load data from files
with open("/Volumes/WD-Elements/Nadine-Dacoff/FileA.txt", "r") as file_a, open("/Volumes/WD-Elements/Nadine-Dacoff/FileB.txt", "r") as file_b:
	data_a = file_a.readlines()
	data_b = file_b.readlines()

# Create a dictionary to map old field names to new field names
old_field_names = {}
for line in data_a:
	old_key, old_name = line.strip().split("\t")
	old_field_names[old_key] = old_name

# Create a dictionary to map old field values to new field values
new_field_names = {}
for line in data_b:
	new_key, new_name = line.strip().split("\t")
	new_field_names[new_key] = new_name

# Field Map: Create a dictionary to map the old field keys from FileA to their corresponding field keys in FileB
field_map = {}
for old_key, old_name in old_field_names.items():
	if old_key in new_field_names:
		new_key = new_field_names[old_key]
		if new_key in new_field_names.values():
			field_map[old_name] = new_key

# Open PDF input and output files
with open("/Volumes/WD-Elements/Nadine-Dacoff/I-485-Sup-A-Drop.pdf", "rb") as pdf_input_file, open("/Volumes/WD-Elements/Nadine-Dacoff/Updated-Supp-A5.pdf", "wb") as pdf_output_file:
	pdf_reader = PdfReader(pdf_input_file)
	pdf_writer = PdfWriter()
	
	 # Copy all pages from the input file to the output file
	for page_num in range(len(pdf_reader.pages)):
		page = pdf_reader.pages[page_num]
		pdf_writer.add_page(page)
		form_fields = pdf_reader.get_form_text_fields()
		field_names_values = form_fields

# Create a field_name dictionary of source PDF field_names in dict format : {'0.00591': 'AppFamilyName', } etc
		field_names_dic_format = {}
		for dict_key_field_name, dict_key_field_value in field_names_values.items():
			field_names_dic_format[dict_key_field_name] = dict_key_field_value

	 # Loop through all form fields on the current page
	for dict_key_field_name, dict_key_field_value in field_names_values.items():
		if dict_key_field_name in old_field_names.values():
			#old_field_name = list(old_field_names.keys())[list(old_field_names.values()).index(dict_key_field_name)]
			new_field_name = field_map[old_name]
			pdf_writer.update_page_form_field_values(page, {new_field_name: dict_key_field_value})
	pdf_writer.write(pdf_output_file)

print("done")