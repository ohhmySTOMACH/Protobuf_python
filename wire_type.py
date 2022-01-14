#!/usr/bin/env python

# import os
import sys
import base64
import blackboxprotobuf as bbp

from optparse import OptionParser

# # 函数用法
# data = base64.b64decode('KglNb2RpZnkgTWU=')
# print(data)
# message,typedef = bbp.decode_message(data)
# message[5] = 'Modified Me'
# print(message)
# data = bbp.encode_message(message,typedef)
# print(data)


def replace_target_bin(bytes_string):
    for row in bytes_string.get('1'):
        if row.get('1') == b'C_LOGIN_BTN_QQ':
            # Replace the text in dict
            bin_raw = row.get('2')
            print(bin_raw)
            row['2'] = '与QQ好友玩 u1'
        #     print(row)
        # if row.get('2') == '与QQ好友玩':
        #     row['2'] = '与QQ好友玩 u1'
        #     print(row)
        # if row.get('2') == b'\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9':
        #     row['2'] = '与QQ好友玩 u1'
        #     print(row)
    # table = bytes_string.values()
    # for rows in table:
    #     for row in rows:
    #         for value in row.values():
    #             if value == b'\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9':
    #                 value = '与QQ好友玩 u1'
    #         print(row)
    # if isinstance(bytes_string, dict):
    #     for value in bytes_string.values(): # replace based on the value list, not working, should still access through the key, since it is a dictionary type
    #         replace_target_bin(value)
    #         # print(value)
    # elif isinstance(bytes_string, list):
    #     for dictionary in bytes_string:
    #         replace_target_bin(dictionary)
    #         # print(dictionary)
    # elif isinstance(bytes_string, bytes):
    #     if bytes_string == b'\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9':
    #         bytes_string = 'u1'
    #         print(bytes_string)
    #         print("替换成功")
    #         # print(bytes_string)

    # return bytes_string


if __name__ == '__main__':
    bin_filename = 'data/TextClientzh_CN.pbin'
    # Read .pbin file
    data_f = open(bin_filename, 'rb')
    # Remove the header
    bytes_string = data_f.read()
    head = b'com.tencent.nk.xlsRes.table_ClientTextInfo\n'
    bytes_string = bytes_string.replace(head, b'')
    # Decode .pbin file to dict type
    txt_decode, typedef = bbp.decode_message(bytes_string) # 返回的文件数据类型是dict dict of a list of dicts
    f = open("./data/output.txt", "w+")
    f.write(str(txt_decode))
    f.close()
    # print("typedef: ", typedef)
    dict_replaced = replace_target_bin(txt_decode)
    f = open("./data/replace_output.txt", "w+")
    f.write(str(dict_replaced))
    f.close()
    # Encode the dict and update the .pbin file
    msg_encode = bbp.encode_message(dict_replaced, typedef)
    f = open("./data/encode_output.pbin", 'wb+')
    f.write(head + msg_encode)
    f.close()
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
