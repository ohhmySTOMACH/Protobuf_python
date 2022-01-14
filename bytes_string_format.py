import sys
from google.protobuf.internal import wire_format

f = open("./data/TextClientzh_CN.pbin", "rb")
bytes_string = f.read()
f.close()
# print(str(bytes_string))
# print("If C_LOGIN_BTN_QQ exist", bin_array.find(b'QQ@'))
# Find byte array that start with C_LOGIN_BTN_QQ, end with \n, not include \n
# add u1 to the end of the byte array
# Or find the byte array with the start and end index
# replace the specific index
# print("Left Index: ", bytes_string.index(b'C_LOGIN'[:2]))
# print("Right Index: ", bytes_string.count(b'\xa9 '))
# bin_array = bytearray(b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n')
# bin_replaced = bytes_string.replace(bin_array, bin_array + b' u1')
# bin_replaced = bytes_string.replace(
#     b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n',
#     b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9 u1\n')
target = b'\x12\x0e\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n'
try:
    print("Index: ", bytes_string.index(target))
except ValueError:
    print("Target not found")
# string = "与QQ好友玩 u1"
# encode = encode_string(string) # bytes_string type
# bytes_string.replace(target, enocde)
f = open("./data/bin_output.txt", "w")
# print(bytes_string)
f.write(str(bytes_string))
f.close()




