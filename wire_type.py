import os
os()
import blackboxprotobuf as bbp
import base64
import sys

# data = base64.b64decode('KglNb2RpZnkgTWU=')
# message,typedef = bbp.decode_message(data)
#
# message[5] = 'Modified Me'
#
# data = bbp.encode_message(message,typedef)
# print(data)
#
bin_filename = './data/addressbook.data'
txt_filename = './data/addressbook.txt'
f = open(txt_filename, 'r')
data_f = open(bin_filename, 'rb')
txt_data = f.read()
print("text: ", txt_data)
bytes_string = f.read()
decode_txt,typedef = bbp.decode_message(bytes_string)
print(decode_txt, "typedef: ", typedef)
# encode_txt = bbp.encode_message(txt_data,typedef)
# print(encode_txt)
# f.close()

# _get_typedef_for_message