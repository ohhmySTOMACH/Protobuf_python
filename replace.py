import sys
from google.protobuf import message, text_format, text_encoding
import ResTextClient_pb2


# Iterates though all client_text_info in the table_client_text_info and prints info about them.
def print_target(table_client_text_info):
    for client_text_info in table_client_text_info.rows:
        if client_text_info.HasField('key'):
            print("Key: ", client_text_info.key)
        if client_text_info.HasField('zh_CN'):
            print("zh_CN: ", client_text_info.zh_CN)
        else:
            print("Message 不存在")


# Replace the byte string in the target binary file
def replace_target(table_client_text_info):
    for client_text_info in table_client_text_info.rows:
        # if key == "C_LOGIN_BTN_QQ" replace zh_CN with "与QQ好友玩 u1"
        if client_text_info.key == "C_LOGIN_BTN_QQ":
            # replace_string = client_text_info.zh_CN + "u1"
            client_text_info.zh_CN = "与QQ好友玩 u1"
            print("字符串已替换成功")


# Replace the byte string not depends on the .proto file
def replace_target_bin(bytes_string):
    # bin_array = bytearray(b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9')
    # bin_replaced = bin_array + b' u1'
    bin_replaced = bytes_string.replace(
        b'\x0eC_LOGIN_BTN_QQ\x12\x0e\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n',
        b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9 u1\n')
    print("字符串已替换成功")
    return bin_replaced


# Main Body
if len(sys.argv) != 2:
    print("使用方法:", sys.argv[0], "文件名")
    sys.exit(-1)

# Read bytes from the binary file
try:
    f = open(sys.argv[1], "rb")
    bytes_string = f.read()
    f.close()
    # Remove Head Before Parsing
    head = b'com.tencent.nk.xlsRes.table_ClientTextInfo\n'
    bytes_string = bytes_string.replace(head, b'')
    # print(bin_array)
except FileNotFoundError:
    print("该文件不存在")
    sys.exit(-1)

# print_target(table_client_text_info)
choice = input("选择替换文本的方法：\n1. 依赖proto   \n2. 不依赖proto \n请输入 1 或 2: ")
while choice:
    if choice == '1':
        table_client_text_info = ResTextClient_pb2.table_ClientTextInfo()
        table_client_text_info.ParseFromString(bytes_string)
        print("反序列化成功")
        # print(table_client_text_info)
        # Replace the string depends on the .proto file
        replace_target(table_client_text_info)
        final_bytes = head + table_client_text_info.SerializeToString()
        f = open(sys.argv[1], "wb")
        f.write(final_bytes)
        f.close()
        break
    elif choice == '2':
        # Replace the string not depend on the .proto file
        bin_replaced = replace_target_bin(bytes_string)
        final_bytes = head + bin_replaced
        f = open(sys.argv[1], "wb")
        f.write(final_bytes)
        f.close()
        break
    else:
        choice = input("输入错误，请重新输入：")