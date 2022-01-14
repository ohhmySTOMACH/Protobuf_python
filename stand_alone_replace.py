# encoding: utf-8
# -*- coding: utf-8 -*-

import sys
import six
import binascii
import struct
from google.protobuf.internal import wire_format, encoder, decoder


class BlackboxProtobufException(Exception):
    """Base class for excepions raised by Blackbox Protobuf"""

    def __init__(self, message, path=None, *args):
        self.path = path
        super(BlackboxProtobufException, self).__init__(message, *args)

    def set_path(self, path):
        if self.path is None:
            self.path = path


class EncoderException(BlackboxProtobufException, ValueError):
    """Thrown when there is an error encoding a dictionary to a type definition"""

    def __str__(self):
        message = super(EncoderException, self).__str__()
        if self.path is not None:
            message = (
                              "Encountered error encoding field %s: " % "->".join(map(str, self.path))
                      ) + message
        return message


class DecoderException(BlackboxProtobufException, ValueError):
    """Thrown when there is an error decoding a bytestring to a dictionary"""

    def __str__(self):
        message = super(DecoderException, self).__str__()
        if self.path is not None:
            message = (
                              "Encountered error decoding field %s: " % "->".join(map(str, self.path))
                      ) + message
        return message


def encode_string(value):
    try:
        value = six.ensure_text(value)
    except TypeError as exc:
        six.raise_from(
            EncoderException("Error encoding string to message: %r" % value), exc
        )
    return encode_bytes(value)


def decode_string(value, pos):
    """Decode varint for length and then the bytes"""
    length, pos = decode_varint(value, pos)
    end = pos + length
    try:
        # backslash escaping isn't reversible easily
        return value[pos:end].decode("utf-8"), end
    except (TypeError, UnicodeDecodeError) as exc:
        six.raise_from(
            DecoderException("Error decoding UTF-8 string %s" % value[pos:end]), exc
        )


def encode_bytes(value):
    """Encode varint length followed by the string.
    This should also work to encode incoming string values.
    """
    if isinstance(value, bytearray):
        value = bytes(value)
    try:
        value = six.ensure_binary(value)
    except TypeError as exc:
        six.raise_from(
            EncoderException("Error encoding bytes to message: %r" % value), exc
        )
    encoded_length = encode_varint(len(value))
    return encoded_length + value


def _gen_append_bytearray(arr):
    def _append_bytearray(x):
        if isinstance(x, (str, int)):
            arr.append(x)
        elif isinstance(x, bytes):
            arr.extend(x)
        else:
            raise EncoderException("Unknown type returned by protobuf library")

    return _append_bytearray


def encode_varint(value):
    """Encode a long or int into a bytearray."""
    output = bytearray()
    if value > (2 ** 63) or value < -(2 ** 63):
        raise EncoderException("Value %d above maximum varint size" % value)
    try:
        encoder._EncodeSignedVarint(_gen_append_bytearray(output), value)
    except (struct.error, ValueError) as exc:
        six.raise_from(
            EncoderException("Error encoding %d as signed varint." % value), exc
        )
    return output


def decode_varint(buf, pos):
    """Decode bytearray into a long."""
    # Convert buffer to string
    if six.PY2:
        buf = str(buf)
    try:
        value, pos = decoder._DecodeSignedVarint(buf, pos)
    except (TypeError, IndexError, decoder._DecodeError) as exc:
        six.raise_from(
            DecoderException(
                "Error decoding varint from %s..."
                % binascii.hexlify(buf[pos: pos + 8])
            ),
            exc,
        )
    return (value, pos)


# Replace the byte string not depends on the .proto file
def replace_target_bin(bytes_string):
    # for row in bytes_string.get('1'):
    #     if row.get('1') == b'C_LOGIN_BTN_QQ':
    #         # Replace the text in dict
    #         row.get('2')
    #         # print(bin_raw)
    #         row['2'] = '与QQ好友玩 u1'
    #         # print(row)
    #         print("字符串已替换成功")
    pass


def run():
    # Read bytes from the binary file
    try:
        file_name = sys.argv[1]
        f = open(file_name, "rb")
        bytes_string = f.read()
        f.close()
        # Remove Head Before Parsing
        head = b'com.tencent.nk.xlsRes.table_ClientTextInfo\n'
        bytes_string = bytes_string.replace(head, b'')
        # print(bin_array)
    except IOError:
        print("The file is not exist")
        sys.exit(-1)

    # # Decode .pbin file
    # txt_decode, typedef = decode_string(bytes_string)  # 返回的文件数据类型是dict dict of a list of dicts
    # print(f'{file_name} 解码成功')
    # replace_target_bin(txt_decode)
    # # Encode the dict and update the .pbin file
    # msg_encode = encode_string(txt_decode, typedef)
    # f = open(file_name, 'wb')
    # f.write(head + msg_encode)
    # f.close()
    target = b'\x12\x0e\xe4\xb8\x8eQQ\xe5\xa5\xbd\xe5\x8f\x8b\xe7\x8e\xa9'
    print("Index: ", bytes_string.index(target))
    string = "与QQ好友玩 u1"
    txt_encoded = encode_string(string)  # bytes_string type
    # print(txt_encoded)
    bin_replaced = bytes_string.replace(target, txt_encoded)
    # f = open("./data/replace_output.txt", 'wb')
    f = open(file_name, 'wb')
    f.write(head + bin_replaced)
    f.close()


# Main Body
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)
    # print(sys.argv)
    run()
