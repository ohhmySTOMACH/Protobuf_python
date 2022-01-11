import os
os.system("protoc ./ResTextClient.proto  --python_out=./")
import blackboxprotobuf as bbp
import base64
import sys
from  google.protobuf import json_format

# 函数用法
# data = base64.b64decode('KglNb2RpZnkgTWU=')
# print(data)
# message,typedef = bbp.decode_message(data)
#
# message[5] = 'Modified Me'
#
# data = bbp.encode_message(message,typedef)
# print(data)

bin_filename = 'data/TextClientzh_CN.pbin'
# txt_filename = 'data/addressbook.dict'

# f = open(txt_filename, 'r')
# txt_data = f.read()
# print("text: ", txt_data)

# Read .pbin file
data_f = open(bin_filename, 'rb')

# Remove the header
bytes_string = data_f.read()
head = b'com.tencent.nk.xlsRes.table_ClientTextInfo\n'
bytes_string = bytes_string.replace(head, b'')
decode_txt,typedef = bbp.decode_message(bytes_string) # 返回的文件是dict数据类型 dict of a list of dict
# f = open("output.txt", "w+")
# f.write(str(decode_txt))
# print(decode_txt, "typedef: ", typedef)
if decode_txt[0].getvalue =


# import pickle
#
# dictionary = {'geek': 1, 'supergeek': True, 4: 'geeky'}
#
# try:
# 	geeky_file = open('geekyfile', 'wb')
# 	pickle.dump(dictionary, geeky_file)
# 	geeky_file.close()
#
# except:
# 	print("Something went wrong")


# Encode
# encode_txt = bbp.encode_message(txt_data,typedef)
# print(encode_txt)
# f.close()
