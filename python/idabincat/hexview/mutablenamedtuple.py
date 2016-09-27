# -*- coding: utf8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is derived from work by Willi Ballenthin
# Downloaded from https://github.com/williballenthin/python-pyqt5-hexview
#
# Modified by Raphaël Rigo <raphael.rigo@airbus.com>
"""
mutablenamedtuple is like collections.namedtuple, but the fields
may be modified. This makes it basically a record type.

Desired usage:
    F = mutablenamedtuple("F", ["foo", "bar", "baz"])
    f = F(1, bar=2, baz=3)
    f.baz = 9
    print(f)
    --> "F(foo=1, bar=2, baz=9)"
"""


def _mutablenamedtuple__init(self, *args, **kwargs):
    super(self.__class__, self).__init__()
    if len(args) > len(self.__fields__):
        raise RuntimeError("Too many arguments provided to {classname}.__init__".format(
                           classname=self.__class__.__name__))

    for i, arg in enumerate(args):
        setattr(self, self.__fields__[i], arg)

    for k, v in kwargs.items():
        if k not in self.__fields__:
            raise RuntimeError("{fieldname} not a valid field in {classname}".format(
                               fieldname=k, classname=self.__class__.__name__))
        setattr(self, k, v)


def _mutablenamedtuple__str(self):
    formatted_fields = []
    for k in self.__fields__:
        v = getattr(self, k)

        formatted_v = str(v)
        if len(formatted_v) > 0xa:
            formatted_v = formatted_v[:0xa] + "..."

        formatted_fields.append("{key}={value}".format(key=k, value=formatted_v))
    return "{classname}({values})".format(classname=self.__class__.__name__,
                                          values=", ".join(formatted_fields))


def mutablenamedtuple(name, fields):
    fs = {f: None for f in fields}
    fs["__fields__"] = fields[:]
    fs["__init__"] = _mutablenamedtuple__init
    fs["__str__"] = _mutablenamedtuple__str
    fs["__repr__"] = _mutablenamedtuple__str
    t = type(name, (object,), fs)
    return t

