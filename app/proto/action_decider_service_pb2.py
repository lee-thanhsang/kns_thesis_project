# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/action_decider_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"proto/action_decider_service.proto\x12\x11\x61\x63tion.decider.v1\"\x1c\n\x0b\x44ialogState\x12\r\n\x05state\x18\x01 \x01(\x0c\" \n\x0e\x41\x63tionResponse\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t2a\n\tACService\x12T\n\rActionDecider\x12\x1e.action.decider.v1.DialogState\x1a!.action.decider.v1.ActionResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.action_decider_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DIALOGSTATE._serialized_start=57
  _DIALOGSTATE._serialized_end=85
  _ACTIONRESPONSE._serialized_start=87
  _ACTIONRESPONSE._serialized_end=119
  _ACSERVICE._serialized_start=121
  _ACSERVICE._serialized_end=218
# @@protoc_insertion_point(module_scope)
