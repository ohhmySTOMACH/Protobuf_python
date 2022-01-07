import sys

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
    sys.exit(-1)
# Print binary array
try:
    f = open(sys.argv[1], "rb")
    bytes_string = f.read()
    f.close()
    print(bytes_string)
    # print("If C_LOGIN_BTN_QQ exist", bin_array.find(b'QQ@'))
    # Find byte array that start with C_LOGIN_BTN_QQ, end with \n, not include \n
    # add u1 to the end of the byte array
    # Or find the byte array with the start and end index
    # replace the specific index
    print("Left Index: ", bytes_string.index(b'C_LOGIN'[:2]))
    print("Right Index: ", bytes_string.count(b'\xa9 '))
    # bin_array = bytearray(b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n')
    # bin_replaced = bytes_string.replace(bin_array, bin_array + b' u1')
    # bin_replaced = bytes_string.replace(
    #     b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9\n',
    #     b'\x0eC_LOGIN_BTN_QQ\x12\x11\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9 u1\n')
    # f = open(sys.argv[1], "wb")
    # print(bin_replaced)
    # f.write(bin_replaced)
    # f.close()
except FileNotFoundError:
    print("该文件不存在")
    sys.exit(-1)
