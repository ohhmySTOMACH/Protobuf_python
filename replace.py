# encoding: utf-8
# -*- coding: utf-8 -*-
import sys
import os
from optparse import OptionParser
# from google.protobuf import message, text_format, text_encoding

print("sys.path", sys.path)
current_dir = os.path.abspath(os.path.dirname('__file__'))
print("replace.py current dir: ", current_dir)
sys.path.append(current_dir)


# Helper Function:
# Iterates though all client_text_info in the table_client_text_info and prints info about them.
def print_target(table_client_text_info):
    for client_text_info in table_client_text_info.rows:
        if client_text_info.HasField('key'):
            print("Key: ", client_text_info.key)
        if client_text_info.HasField('zh_CN'):
            print("zh_CN: ", client_text_info.zh_CN)
        else:
            print("message DOES NOT EXIST")


# Replace the byte string in the target binary file
def replace_target(table_client_text_info):
    for client_text_info in table_client_text_info.rows:
        if client_text_info.key == "C_LOGIN_BTN_QQ":
            # replace_string = client_text_info.zh_CN + "u1"
            client_text_info.zh_CN = "与QQ好友玩 u1"
            print("REPLACE COMPLETE!!")


# 此处可考虑改进成递归遍历的结构，不使用key:1, key:2
# Replace the byte string not depends on the .proto file
def replace_target_bin(bytes_string):
    for row in bytes_string.get('1'):
        if row.get('1') == b'C_LOGIN_BTN_QQ':
            # Replace the text in dict
            # print(bin_raw)
            row['2'] = '与QQ好友玩 u1'
            # print(row)
            print("REPLACE COMPLETE!!")


def load_parameter():
    parser = OptionParser(usage="usage: replace.py [options] file_name", add_help_option=False)

    parser.add_option("-h", "--help", action="help", help="show this help message and exit")
    parser.add_option("-p", "--protobuf", help="依赖proto替换文本")
    parser.add_option("-w", "--wiretype", help="不依赖proto,基于wire type替换文本")

    options, args = parser.parse_args()
    # print(options, args)
    return options


def run(options):
    # Read bytes from the binary file
    try:
        file_name = sys.argv[2]
        f = open(file_name, "rb")
        bytes_string = f.read()
        f.close()
        # Remove Head Before Parsing
        head = b'com.tencent.nk.xlsRes.table_ClientTextInfo\n'
        bytes_string = bytes_string.replace(head, b'')
        # print(bin_array)
    except IOError:
        print("FILE DOES NOT EXIST")
        sys.exit(-1)

    if options.protobuf:
        import ResTextClient_pb2

        table_client_text_info = ResTextClient_pb2.table_ClientTextInfo()
        table_client_text_info.ParseFromString(bytes_string)
        print("{0} PARSING DONE!".format(file_name))
        # print(table_client_text_info)
        # Replace the string depends on the .proto file
        replace_target(table_client_text_info)
        final_bytes = head + table_client_text_info.SerializeToString()
        f = open(file_name, "wb")
        f.write(final_bytes)
        f.close()
    elif options.wiretype:
        import blackboxprotobuf as bbp
        # Decode .pbin file to dict type
        txt_decode, typedef = bbp.decode_message(bytes_string)  # 返回的文件数据类型是dict dict of a list of dicts
        print("{0} DECODE DONE!".format(file_name))
        replace_target_bin(txt_decode)
        # Encode the dict and update the .pbin file
        msg_encode = bbp.encode_message(txt_decode, typedef)
        f = open(file_name, 'wb')
        f.write(head + msg_encode)
        f.close()


# Main Body
if __name__ == '__main__':
    if len(sys.argv) < 3:
        load_parameter()
        sys.exit(-1)
    # print(sys.argv)
    options = load_parameter()
    run(options)

