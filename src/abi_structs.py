from .hextools import ( add0x,
                        bytes_to_hex,
                        bytes_to_string,
                        hex_to_bytes,
                        to_hex,
                        trim0x, )

from .keccak import keccak
from .types import Types

import eth_abi
import logging
from functools import partial


log = logging.getLogger(__name__)


class ABIContract(object):
    __slots__=["_functions","_events","_constructor","_fallback","_functions_by_selector","_events_by_topic","_bytecode","_address"]

    def __init__(self, abi):
        functions = [ABIFunction(f) for f in abi if f["type"] == "function"]
        events = [ABIEvent(f) for f in abi if f["type"] == "event"]
        """if bytecode:
            constructor = [ABIConstructor(f) for f in abi if f["type"] == "constructor"]
            assert len(constructor) == 1, "Too many constructors"
            self._constructor = constructor[0]
            self._bytecode = bytecode
        else:
            self._constructor = None
            self._bytecode = None"""
        fallback = [f for f in abi if f["type"] == "fallback"]
        assert len(fallback) <= 1, "Too many fallback functions"
        if len(fallback) == 1:
            self._fallback = fallback[0]
        else:
            fallback = None
        #TODO handle function overloading! This is blocked by creating
        #strong typing system for all fundamental types!
        #function_names = [function.name for function in functions]
        #function_name_counts = [name for name in function_names if function_names.count(name) > 1]
        #name_indices = [i for i, x in enumerate(function_name_counts) if name == Name]
        self._functions = {f.name:f for f in functions}
        self._functions_by_selector = {f.function_selector:f for f in functions}
        self._events = {e.name:e for e in events}
        self._events_by_topic = {e.topic.as_str():e for e in events}

    def _encode_function_selector(self,name,types):
        func_string = '{}({})'.format(name,','.join(types))
        return Types.bytes4(add0x(keccak(to_hex(func_string))[0:10]))

    @property
    def constructor(self):
        return self._constructor

    @property
    def bytecode(self):
        return self._bytecode

    @property
    def fallback(self):
        return self._fallback

    @property
    def functions(self):
        return self._functions

    @property
    def functions_by_selector(self):
        return self._functions_by_selector

    @property
    def events(self):
        return self._events

    @property
    def events_by_topic(self):
        return self._events_by_topic

    @property
    def address(self):
        return self._address

    @property
    def select(self):
        return self._encode_function_selector(types)

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIFunction(object):
    __slots__=["_constant","_name","_stateMutability","_inputs","_outputs","_payable","_encode","_decode","_function_selector"]

    def __init__(self,abi):
        self._inputs = [ABIFunctionInput(item) for item in abi["inputs"]]
        self._outputs = [ABIFunctionOutput(item) for item in abi["outputs"]]
        self._name = abi["name"]
        self._constant = abi["constant"]
        assert type(self._constant) is bool
        self._stateMutability = abi["stateMutability"]
        self._payable = abi["payable"]
        self._function_selector = self._encode_function_selector()
        self._decode = self._parse_return_data
        self._encode = self._build_call_data

    def _encode_function_selector(self):
        types = [element.type_ for element in self._inputs]
        func_string = '{}({})'.format(self._name,','.join(types))
        return Types.bytes4(add0x(keccak(to_hex(func_string))[0:10]))

    def _parse_return_data(self, data):
        names = [element.name for element in self._outputs]
        types = [element.type_.lower() for element in self._outputs]
        values = eth_abi.decode_abi(types, hex_to_bytes(data))
        log.debug('in _parse_return_data VALUES PARSED AS {}'.format(values))
        def try_getattr(name):
            try:
                return Types.safeLookup(name)
            except AttributeError:
                return None
        type_constructors = [try_getattr(t) for t in types]
        values = [type_constructors[i](v) if type_constructors[i] else v for i, v in enumerate(values)]
        values = [bytes_to_string(v) if types[i]=="string" else v for i,v in enumerate(values)]
        if len(values) > 1:
            return dict(zip(names,values))
        else:
            return values[0]

    def _build_call_data(self, values):
        func_string = self._function_selector
        types = [element.type_ for element in self._inputs]
        def try_getattr(name):
            try:
                return Types.safeLookup(name)
            except AttributeError:
                return None
        type_constructors = [try_getattr(t) for t in types]
        values = [v.encode() if type_constructors[i] else v for i,v in enumerate(values)]
        return add0x(trim0x(func_string.as_str()) + bytes_to_hex(eth_abi.encode_abi(types,values)))

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self.outputs

    @property
    def name(self):
        return self._name

    @property
    def constant(self):
        return self._constant

    @property
    def stateMutability(self):
        return self._stateMutability

    @property
    def payable(self):
        return self._payable

    @property
    def function_selector(self):
        return self._function_selector

    @property
    def encode(self):
        return self._encode

    @property
    def decode(self):
        return self._decode

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIFunctionInput(object):
    __slots__=["_name","_type"]
    def __init__(self,inpt):
        self._name = inpt["name"]
        self._type = inpt["type"]

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIFunctionOutput(object):
    __slots__=["_name","_type"]

    def __init__(self,inpt):
        self._name = inpt["name"]
        self._type = inpt["type"]

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIEvent(object):
    __slots__=["_anonymous","_name","_inputs","_topic","_decode","_name"]
    def __init__(self, abi):
        #TODO CREATE PARSED EVENT OBJECT FOR THE RETURN FROM decode
        self._name = abi["name"]
        self._inputs = [ABIEventInput(item) for item in abi["inputs"]]
        self._topic = self._encode_event_topic(abi)
        self._decode = partial(self._parse_event, abi)

    def _encode_event_topic(self,abi):
        types = [element["type"] for element in abi["inputs"]]
        event_string = '{}({})'.format(self._name,','.join(types))
        return Types.bytes32(keccak(to_hex(event_string)))

    def _is_valid_event_abi_naming_scheme(self,event_abi):
        #TODO duplicate logic! cleanup!
        event_inputs = event_abi["inputs"]
        #build topics abi and data abi names
        log_topics_abi = [element for element in event_inputs if element["indexed"]]
        log_topic_names = [element["name"] for element in log_topics_abi]
        log_data_abi = [element for element in event_inputs if not element["indexed"]]
        log_data_names = [element["name"] for element in log_data_abi]

        # sanity check that there are not name intersections between the topic
        # names and the data argument names.
        if set(log_topic_names).intersection(log_data_names):
            return False
        else:
            return True

    def _parse_event(self,event_abi, log_entry):
        #get log data and log topics from log
        if event_abi['anonymous']:
            log_topics = log_entry.topics
        else:
            log_topics = log_entry.topics[1:]
        log_data = log_entry.data

        event_inputs = event_abi["inputs"]

        assert self._is_valid_event_abi_naming_scheme(event_abi)

        #build topics abi and data abi names/types
        log_topics_abi = [element for element in event_inputs if element["indexed"]]
        log_topic_types = [element["type"] for element in log_topics_abi]
        log_topic_names = [element["name"] for element in log_topics_abi]
        log_data_abi = [element for element in event_inputs if not element["indexed"]]
        log_data_types = [element["type"] for element in log_data_abi]
        log_data_names = [element["name"] for element in log_data_abi]

        #sanity check length of topics
        if len(log_topics) != len(log_topic_types):
            return None
        def try_getattr(name):
            try:
                return Types.safeLookup(name)
            except AttributeError:
                return None
        #encode to bytes object for eth_abi
        encoded_topics = [hex_to_bytes(x) for x in log_topics]
        #parse values from topics
        log_topic_values = [eth_abi.decode_single(t, v) for t, v in zip(log_topic_types, encoded_topics)]
        type_constructors = [try_getattr(t) for t in log_topic_types]
        log_topic_values = [type_constructors[i[0]](log_topic_values[i[0]]) if type_constructors[i[0]] else log_topic_values[i[0]] for i in enumerate(log_topic_values)]
        #build topic event object with names
        event_topic_obj = dict(zip(log_topic_names,log_topic_values))
        #parse event values from data
        log_data_values = eth_abi.decode_abi(log_data_types,hex_to_bytes(log_entry.data))
        type_constructors = [try_getattr(t) for t in log_data_types]
        log_data_values = [type_constructors[i[0]](log_data_values[i[0]]) if type_constructors[i[0]] else log_data_values[i[0]] for i in enumerate(log_data_values)]
        #build data event object with names
        event_data_obj = dict(zip(log_data_names,log_data_values))
        #combine objects
        parsed_event = {}
        parsed_event.update(event_data_obj)
        parsed_event.update(event_topic_obj)
        event = {"name":self._name,"event":parsed_event}
        #return the combined result
        return event

    @property
    def topic(self):
        return self._topic

    @property
    def decode(self):
        return self._decode

    @property
    def name(self):
        return self._name

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIEventInput(object):
    __slots__=["_indexed","_name","_type"]

    def __init__(self,inpt):
        self._name = inpt["name"]
        self._type = inpt["type"]
        self._indexed = inpt["indexed"]
        assert type(self._indexed) is bool

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    @property
    def indexed(self):
        return self._type

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIConstructor(object):
    ["_stateMutability","_inputs","_payable","_encode"]

    def __init__(self,abi):
        self._stateMutability = abi["stateMutability"]
        self._inputs = abi["inputs"]
        self._payable = abi["payable"]
        #TODO handle contract deployment
        #self._encode = partial()

    def _build_call_data(self, abi, args):
        func_string = self._function_selector
        types = [element["type"] for element in abi["inputs"]]
        def try_getattr(name):
            try:
                return Types.safeLookup(name)
            except AttributeError:
                return None
        type_constructors = [try_getattr(t) for t in types]
        values = [hex_to_bytes(str(values[i[0]])) if type_constructors[i[0]] else values[i[0]] for i in enumerate(values)]
        eth_abi.encode_abi(types,values)
        return data

    @property
    def stateMutability(self):
        return self._stateMutability

    @property
    def inputs(self):
        return self._inputs

    @property
    def payable(self):
        return self.payable

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))


class ABIFallback(object):
    ["_stateMutability","_payable"]

    def __init__(self,abi):
        self._stateMutability = abi["stateMutability"]
        self._payable = abi["payable"]
        #TODO handle calling fallback?

    @property
    def stateMutability(self):
        return self._stateMutability

    @property
    def payable(self):
        return self._payable

    def as_dict(self):
        values = [getattr(self,v) for v in self.__slots__]
        names = [n[1:] for n in self.__slots__]
        return dict(zip(names, values))
