# encoding: utf-8
# -*- coding: utf-8 -*-

# Compatible with python27

import sys
import six
import binascii
import struct
import logging
import copy
from google.protobuf.internal import encoder, decoder, wire_format


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


class Config:
    def __init__(self):

        # Map of message type names to typedefs, previously stored at
        # `blackboxprotobuf.known_messages`
        self.known_types = {}

        # Default type for "bytes" like objects that aren't messages or strings
        # Other option is currently just 'bytes_hex'
        self.default_binary_type = "bytes"

        # Change the default type for a wiretype (eg.
        self.default_types = {}

    def get_default_type(self, wiretype):
        default_type = self.default_types.get(wiretype, None)
        if default_type is None:
            default_type = type_maps.WIRE_TYPE_DEFAULTS.get(wiretype, None)

        return default_type


def decode(buf, message_type=None, config=None):
    """Decode a message to a Python dictionary.
    Returns tuple of (values, types)
    """

    if config is None:
        config = Config()

    if isinstance(buf, bytearray):
        buf = bytes(buf)
    buf = six.ensure_binary(buf)
    if message_type is None or isinstance(message_type, str):
        if message_type not in config.known_types:
            message_type = {}
        else:
            message_type = config.known_types[message_type]

    value, typedef, _ = decode_message(
        buf, config, message_type
    )
    return value, typedef


# TODO add explicit validation of values to message type
def encode(value, message_type, config=None):
    """Encodes a python dictionary to a message.
    Returns a bytearray
    """

    if config is None:
        config = Config()
    return bytes(
        encode_message(
            value, config, message_type
        )
    )


def encode_message(data, config, typedef, path=None):
    """Encode a Python dictionary representing a protobuf message
    data - Python dictionary mapping field numbers to values
    typedef - Type information including field number, field name and field type
    This will throw an exception if an unkown value is used as a key
    """
    output = bytearray()
    if path is None:
        path = []

    for field_number, value in data.items():
        # Get the field number convert it as necessary
        alt_field_number = None

        if six.PY2:
            string_types = (str, unicode)
        else:
            string_types = str

        if isinstance(field_number, string_types):
            if "-" in field_number:
                field_number, alt_field_number = field_number.split("-")
            # TODO can refactor to cache the name to number mapping
            for number, info in typedef.items():
                if (
                        "name" in info
                        and info["name"] == field_number
                        and field_number != ""
                ):
                    field_number = number
                    break
        else:
            field_number = str(field_number)

        field_path = path[:]
        field_path.append(field_number)

        if field_number not in typedef:
            raise EncoderException(
                "Provided field name/number %s is not valid" % (field_number),
                field_path,
            )

        field_typedef = typedef[field_number]

        # Get encoder
        if "type" not in field_typedef:
            raise TypedefException(
                "Field %s does not have a defined type." % field_number, field_path
            )

        field_type = field_typedef["type"]

        field_encoder = None
        if alt_field_number is not None:
            if alt_field_number not in field_typedef["alt_typedefs"]:
                raise EncoderException(
                    "Provided alt field name/number %s is not valid for field_number %s"
                    % (alt_field_number, field_number),
                    field_path,
                )
            if isinstance(field_typedef["alt_typedefs"][alt_field_number], dict):
                innertypedef = field_typedef["alt_typedefs"][alt_field_number]
                field_encoder = lambda data: encode_lendelim_message(
                    data, config, innertypedef, path=field_path
                )

            else:
                # just let the field
                field_type = field_typedef["alt_typedefs"][alt_field_number]

        if field_encoder is None:
            if field_type == "message":
                innertypedef = None
                if "message_typedef" in field_typedef:
                    innertypedef = field_typedef["message_typedef"]
                elif "message_type_name" in field_typedef:
                    message_type_name = field_typedef["message_type_name"]
                    if message_type_name not in config.known_types:
                        raise TypedefException(
                            "Message type (%s) has not been defined"
                            % field_typedef["message_type_name"],
                            field_path,
                        )
                    innertypedef = config.known_types[message_type_name]
                else:
                    raise TypedefException(
                        "Could not find message typedef for %s" % field_number,
                        field_path,
                    )

                field_encoder = lambda data: encode_lendelim_message(
                    data, config, innertypedef, path=field_path
                )
            else:
                if field_type not in blackboxprotobuf.lib.types.ENCODERS:
                    raise TypedefException("Unknown type: %s" % field_type)
                field_encoder = blackboxprotobuf.lib.types.ENCODERS[field_type]
                if field_encoder is None:
                    raise TypedefException(
                        "Encoder not implemented for %s" % field_type, field_path
                    )

        # Encode the tag
        tag = encoder.TagBytes(
            int(field_number), blackboxprotobuf.lib.types.WIRETYPES[field_type]
        )

        try:
            # Handle repeated values
            if isinstance(value, list) and not field_type.startswith("packed_"):
                for repeated in value:
                    output += tag
                    output += field_encoder(repeated)
            else:
                output += tag
                output += field_encoder(value)
        except EncoderException as exc:
            exc.set_path(field_path)
            six.reraise(*sys.exc_info())

    return output


def decode_message(buf, config, typedef=None, pos=0, end=None, depth=0, path=None):
    """Decode a protobuf message with no length delimiter"""
    # TODO recalculate and re-add path for errors
    if end is None:
        end = len(buf)

    logging.debug("End: %d", end)
    if typedef is None:
        typedef = {}
    else:
        # Don't want to accidentally modify the original
        typedef = copy.deepcopy(typedef)

    if path is None:
        path = []

    output = {}

    grouped_fields, pos = _group_by_number(buf, pos, end, path)
    for (field_number, (wire_type, buffers)) in grouped_fields.items():
        # wire_type should already be validated by _group_by_number

        path = path[:] + [field_number]
        field_outputs = None
        field_typedef = typedef.get(field_number, {})
        field_key = _get_field_key(field_number, typedef, path)
        # Easy cases. Fixed size or bytes/string
        if (
            wire_type
            in [
                wire_format.WIRETYPE_FIXED32,
                wire_format.WIRETYPE_FIXED64,
                wire_format.WIRETYPE_VARINT,
            ]
            or ("type" in field_typedef and field_typedef["type"] != "message")
        ):

            if "type" not in field_typedef:
                field_typedef["type"] = config.get_default_type(wire_type)
            else:
                # have a type, but make sure it matches the wiretype
                if (
                    blackboxprotobuf.lib.types.WIRETYPES[field_typedef["type"]]
                    != wire_type
                ):
                    raise DecoderException(
                        "Type %s from typedef did not match wiretype %s for "
                        "field %s" % (field_typedef["type"], wire_type, field_key),
                        path=path,
                    )

            # we already have a type, just map the decoder
            if field_typedef["type"] not in blackboxprotobuf.lib.types.DECODERS:
                raise TypedefException(
                    "Got unkown type %s for field_number %s"
                    % (field_typedef["type"], field_number),
                    path=path,
                )

            decoder = blackboxprotobuf.lib.types.DECODERS[field_typedef["type"]]
            field_outputs = [decoder(buf, 0) for buf in buffers]

            # this shouldn't happen, but let's check just in case
            for buf, _pos in zip(buffers, [y for _, y in field_outputs]):
                assert len(buf) == _pos

            field_outputs = [value for (value, _) in field_outputs]
            if len(field_outputs) == 1:
                output[field_key] = field_outputs[0]
            else:
                output[field_key] = field_outputs

        elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
            _try_decode_lendelim_fields(
                buffers, field_key, field_typedef, output, config
            )

        # Save the field typedef/type back to the typedef
        typedef[field_number] = field_typedef

    return output, typedef, pos


# Helper functions: help with encode and decode string, varint and bytes
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


def _group_by_number(buf, pos, end, path):
    """Parse through the whole message and return buffers based on wire type.
    This forces us to parse the whole message at once, but I think we're
    doing that anyway.
    Returns a dictionary like:
        {
            "2": (<wiretype>, [<data>])
        }
    """

    output_map = {}
    while pos < end:
        # Read in a field
        try:
            if six.PY2:
                tag, pos = decoder._DecodeVarint(str(buf), pos)
            else:
                tag, pos = decoder._DecodeVarint(buf, pos)
        except (IndexError, decoder._DecodeError) as exc:
            six.raise_from(
                DecoderException(
                    "Error decoding length from buffer: %r..."
                    % (binascii.hexlify(buf[pos : pos + 8])),
                    path=path,
                ),
                exc,
            )

        field_number, wire_type = wire_format.UnpackTag(tag)

        # We want field numbers as strings everywhere
        field_number = str(field_number)

        path = path[:] + [field_number]

        if field_number in output_map and output_map[field_number][0] != wire_type:
            """This should never happen"""
            raise DecoderException(
                "Field %s has mistmatched wiretypes. Previous: %s Now: %s"
                % (field_number, output_map[field_number][0], wire_type),
                path=path,
            )

        length = None
        if wire_type == wire_format.WIRETYPE_VARINT:
            # We actually have to read in the whole varint to figure out it's size
            _, new_pos = decode_varint(buf, pos)
            length = new_pos - pos
        elif wire_type == wire_format.WIRETYPE_FIXED32:
            length = 4
        elif wire_type == wire_format.WIRETYPE_FIXED64:
            length = 8
        elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
            # Read the length from the start of the message
            # add on the length of the length tag as well
            bytes_length, new_pos = decode_varint(buf, pos)
            length = bytes_length + (new_pos - pos)
        elif wire_type in [
            wire_format.WIRETYPE_START_GROUP,
            wire_format.WIRETYPE_END_GROUP,
        ]:
            raise DecoderException("GROUP wire types not supported", path=path)
        else:
            raise DecoderException("Got unkown wire type: %d" % wire_type, path=path)
        if pos + length > end:
            raise DecoderException(
                "Decoded length for field %s goes over end: %d > %d"
                % (field_number, pos + length, end),
                path=path,
            )

        field_buf = buf[pos : pos + length]

        if field_number in output_map:
            output_map[field_number][1].append(field_buf)
        else:
            output_map[field_number] = (wire_type, [field_buf])
        pos += length
    return output_map,


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
    for row in bytes_string.get('1'):
        if row.get('1') == b'C_LOGIN_BTN_QQ':
            # Replace the text in dict
            row.get('2')
            # print(bin_raw)
            row['2'] = '与QQ好友玩 u1'
            # print(row)
            print("REPLACE COMPLETE!!")


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
        print("FILE DOES NOT EXIST")
        sys.exit(-1)

    # Decode .pbin file to dict type
    txt_decode, typedef = decode(bytes_string)  # 返回的文件数据类型是dict dict of a list of dicts
    print("{0} DECODE DONE!".format(file_name))
    replace_target_bin(txt_decode)
    # Encode the dict and update the .pbin file
    msg_encode = encode(txt_decode, typedef)
    f = open(file_name, 'wb')
    f.write(head + msg_encode)
    f.close()


# Main Body
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python {0} file_name".format(sys.argv[0]))
        sys.exit(-1)
    # print(sys.argv)
    run()
