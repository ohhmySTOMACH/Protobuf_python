# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: addressbook.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11\x61\x64\x64ressbook.proto\"\xc9\x01\n\x06Person\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 '
    b'\x01(\x05\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12#\n\x06phones\x18\x04 \x03('
    b'\x0b\x32\x13.Person.PhoneNumber\x1a\x44\n\x0bPhoneNumber\x12\x0e\n\x06number\x18\x01 \x01('
    b'\t\x12%\n\x04type\x18\x02 \x01(\x0e\x32\x11.Person.PhoneType:\x04HOME\"+\n\tPhoneType\x12\n\n\x06MOBILE\x10\x00'
    b'\x12\x08\n\x04HOME\x10\x01\x12\x08\n\x04WORK\x10\x02\"&\n\x0b\x41\x64\x64ressBook\x12\x17\n\x06people\x18\x01 '
    b'\x03(\x0b\x32\x07.Person')

_PERSON = DESCRIPTOR.message_types_by_name['Person']
_PERSON_PHONENUMBER = _PERSON.nested_types_by_name['PhoneNumber']
_ADDRESSBOOK = DESCRIPTOR.message_types_by_name['AddressBook']
_PERSON_PHONETYPE = _PERSON.enum_types_by_name['PhoneType']
Person = _reflection.GeneratedProtocolMessageType('Person', (_message.Message,), {

    'PhoneNumber': _reflection.GeneratedProtocolMessageType('PhoneNumber', (_message.Message,), {
        'DESCRIPTOR': _PERSON_PHONENUMBER,
        '__module__': 'addressbook_pb2'
        # @@protoc_insertion_point(class_scope:Person.PhoneNumber)
    })
    ,
    'DESCRIPTOR': _PERSON,
    '__module__': 'addressbook_pb2'
    # @@protoc_insertion_point(class_scope:Person)
})
_sym_db.RegisterMessage(Person)
_sym_db.RegisterMessage(Person.PhoneNumber)

AddressBook = _reflection.GeneratedProtocolMessageType('AddressBook', (_message.Message,), {
    'DESCRIPTOR': _ADDRESSBOOK,
    '__module__': 'addressbook_pb2'
    # @@protoc_insertion_point(class_scope:AddressBook)
})
_sym_db.RegisterMessage(AddressBook)

if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _PERSON._serialized_start = 22
    _PERSON._serialized_end = 223
    _PERSON_PHONENUMBER._serialized_start = 110
    _PERSON_PHONENUMBER._serialized_end = 178
    _PERSON_PHONETYPE._serialized_start = 180
    _PERSON_PHONETYPE._serialized_end = 223
    _ADDRESSBOOK._serialized_start = 225
    _ADDRESSBOOK._serialized_end = 263
# @@protoc_insertion_point(module_scope)
