static void *opcode_targets[256] = {
    &&TARGET_CACHE,
    &&TARGET_BEFORE_ASYNC_WITH,
    &&TARGET_BEFORE_WITH,
    &&TARGET_BINARY_OP_ADD_FLOAT,
    &&TARGET_BINARY_OP_ADD_INT,
    &&TARGET_BINARY_OP_ADD_UNICODE,
    &&TARGET_BINARY_OP_INPLACE_ADD_UNICODE,
    &&TARGET_BINARY_OP_MULTIPLY_FLOAT,
    &&TARGET_BINARY_OP_MULTIPLY_INT,
    &&TARGET_BINARY_OP_SUBTRACT_FLOAT,
    &&TARGET_BINARY_OP_SUBTRACT_INT,
    &&TARGET_BINARY_SLICE,
    &&TARGET_BINARY_SUBSCR,
    &&TARGET_BINARY_SUBSCR_DICT,
    &&TARGET_BINARY_SUBSCR_GETITEM,
    &&TARGET_BINARY_SUBSCR_LIST_INT,
    &&TARGET_BINARY_SUBSCR_STR_INT,
    &&TARGET_RESERVED,
    &&TARGET_BINARY_SUBSCR_TUPLE_INT,
    &&TARGET_CHECK_EG_MATCH,
    &&TARGET_CHECK_EXC_MATCH,
    &&TARGET_CLEANUP_THROW,
    &&TARGET_DELETE_SUBSCR,
    &&TARGET_END_ASYNC_FOR,
    &&TARGET_END_FOR,
    &&TARGET_END_SEND,
    &&TARGET_EXIT_INIT_CHECK,
    &&TARGET_FORMAT_SIMPLE,
    &&TARGET_FORMAT_WITH_SPEC,
    &&TARGET_GET_AITER,
    &&TARGET_GET_ANEXT,
    &&TARGET_GET_ITER,
    &&TARGET_GET_LEN,
    &&TARGET_GET_YIELD_FROM_ITER,
    &&TARGET_INTERPRETER_EXIT,
    &&TARGET_LOAD_ASSERTION_ERROR,
    &&TARGET_LOAD_BUILD_CLASS,
    &&TARGET_LOAD_LOCALS,
    &&TARGET_MAKE_FUNCTION,
    &&TARGET_MATCH_KEYS,
    &&TARGET_MATCH_MAPPING,
    &&TARGET_MATCH_SEQUENCE,
    &&TARGET_NOP,
    &&TARGET_POP_EXCEPT,
    &&TARGET_POP_TOP,
    &&TARGET_PUSH_EXC_INFO,
    &&TARGET_PUSH_NULL,
    &&TARGET_RETURN_GENERATOR,
    &&TARGET_RETURN_VALUE,
    &&TARGET_SETUP_ANNOTATIONS,
    &&TARGET_STORE_ATTR_INSTANCE_VALUE,
    &&TARGET_STORE_ATTR_SLOT,
    &&TARGET_STORE_SLICE,
    &&TARGET_STORE_SUBSCR,
    &&TARGET_STORE_SUBSCR_DICT,
    &&TARGET_STORE_SUBSCR_LIST_INT,
    &&TARGET_TO_BOOL,
    &&TARGET_TO_BOOL_ALWAYS_TRUE,
    &&TARGET_TO_BOOL_BOOL,
    &&TARGET_TO_BOOL_INT,
    &&TARGET_TO_BOOL_LIST,
    &&TARGET_TO_BOOL_NONE,
    &&TARGET_TO_BOOL_STR,
    &&TARGET_UNARY_INVERT,
    &&TARGET_UNARY_NEGATIVE,
    &&TARGET_UNARY_NOT,
    &&TARGET_WITH_EXCEPT_START,
    &&TARGET_BINARY_OP,
    &&TARGET_BUILD_CONST_KEY_MAP,
    &&TARGET_BUILD_LIST,
    &&TARGET_BUILD_MAP,
    &&TARGET_BUILD_SET,
    &&TARGET_BUILD_SLICE,
    &&TARGET_BUILD_STRING,
    &&TARGET_BUILD_TUPLE,
    &&TARGET_CALL,
    &&TARGET_CALL_BOUND_METHOD_EXACT_ARGS,
    &&TARGET_CALL_BUILTIN_CLASS,
    &&TARGET_CALL_BUILTIN_FAST_WITH_KEYWORDS,
    &&TARGET_CALL_FUNCTION_EX,
    &&TARGET_CALL_INTRINSIC_1,
    &&TARGET_CALL_INTRINSIC_2,
    &&TARGET_CALL_METHOD_DESCRIPTOR_FAST_WITH_KEYWORDS,
    &&TARGET_CALL_NO_KW_ALLOC_AND_ENTER_INIT,
    &&TARGET_CALL_NO_KW_BUILTIN_FAST,
    &&TARGET_CALL_NO_KW_BUILTIN_O,
    &&TARGET_CALL_NO_KW_ISINSTANCE,
    &&TARGET_CALL_NO_KW_LEN,
    &&TARGET_CALL_NO_KW_LIST_APPEND,
    &&TARGET_CALL_NO_KW_METHOD_DESCRIPTOR_FAST,
    &&TARGET_CALL_NO_KW_METHOD_DESCRIPTOR_NOARGS,
    &&TARGET_CALL_NO_KW_METHOD_DESCRIPTOR_O,
    &&TARGET_CALL_NO_KW_STR_1,
    &&TARGET_CALL_NO_KW_TUPLE_1,
    &&TARGET_CALL_NO_KW_TYPE_1,
    &&TARGET_CALL_PY_EXACT_ARGS,
    &&TARGET_CALL_PY_WITH_DEFAULTS,
    &&TARGET_COMPARE_OP,
    &&TARGET_COMPARE_OP_FLOAT,
    &&TARGET_COMPARE_OP_INT,
    &&TARGET_COMPARE_OP_STR,
    &&TARGET_CONTAINS_OP,
    &&TARGET_CONVERT_VALUE,
    &&TARGET_COPY,
    &&TARGET_COPY_FREE_VARS,
    &&TARGET_DELETE_ATTR,
    &&TARGET_DELETE_DEREF,
    &&TARGET_DELETE_FAST,
    &&TARGET_DELETE_GLOBAL,
    &&TARGET_DELETE_NAME,
    &&TARGET_DICT_MERGE,
    &&TARGET_DICT_UPDATE,
    &&TARGET_ENTER_EXECUTOR,
    &&TARGET_EXTENDED_ARG,
    &&TARGET_FOR_ITER,
    &&TARGET_FOR_ITER_GEN,
    &&TARGET_FOR_ITER_LIST,
    &&TARGET_FOR_ITER_RANGE,
    &&TARGET_FOR_ITER_TUPLE,
    &&TARGET_GET_AWAITABLE,
    &&TARGET_IMPORT_FROM,
    &&TARGET_IMPORT_NAME,
    &&TARGET_IS_OP,
    &&TARGET_JUMP_BACKWARD,
    &&TARGET_JUMP_BACKWARD_NO_INTERRUPT,
    &&TARGET_JUMP_FORWARD,
    &&TARGET_KW_NAMES,
    &&TARGET_LIST_APPEND,
    &&TARGET_LIST_EXTEND,
    &&TARGET_LOAD_ATTR,
    &&TARGET_LOAD_ATTR_CLASS,
    &&TARGET_LOAD_ATTR_GETATTRIBUTE_OVERRIDDEN,
    &&TARGET_LOAD_ATTR_INSTANCE_VALUE,
    &&TARGET_LOAD_ATTR_METHOD_LAZY_DICT,
    &&TARGET_LOAD_ATTR_METHOD_NO_DICT,
    &&TARGET_LOAD_ATTR_METHOD_WITH_VALUES,
    &&TARGET_LOAD_ATTR_MODULE,
    &&TARGET_LOAD_ATTR_NONDESCRIPTOR_NO_DICT,
    &&TARGET_LOAD_ATTR_NONDESCRIPTOR_WITH_VALUES,
    &&TARGET_LOAD_ATTR_PROPERTY,
    &&TARGET_LOAD_ATTR_SLOT,
    &&TARGET_LOAD_ATTR_WITH_HINT,
    &&TARGET_LOAD_CONST,
    &&TARGET_LOAD_DEREF,
    &&TARGET_LOAD_FAST,
    &&TARGET_LOAD_FAST_AND_CLEAR,
    &&TARGET_LOAD_FAST_CHECK,
    &&TARGET_LOAD_FAST_LOAD_FAST,
    &&TARGET_LOAD_FROM_DICT_OR_DEREF,
    &&TARGET_LOAD_FROM_DICT_OR_GLOBALS,
    &&TARGET_LOAD_GLOBAL,
    &&TARGET_LOAD_GLOBAL_BUILTIN,
    &&TARGET_LOAD_GLOBAL_MODULE,
    &&TARGET_LOAD_NAME,
    &&TARGET_LOAD_SUPER_ATTR,
    &&TARGET_LOAD_SUPER_ATTR_ATTR,
    &&TARGET_LOAD_SUPER_ATTR_METHOD,
    &&TARGET_MAKE_CELL,
    &&TARGET_MAP_ADD,
    &&TARGET_MATCH_CLASS,
    &&TARGET_POP_JUMP_IF_FALSE,
    &&TARGET_POP_JUMP_IF_NONE,
    &&TARGET_POP_JUMP_IF_NOT_NONE,
    &&TARGET_POP_JUMP_IF_TRUE,
    &&TARGET_RAISE_VARARGS,
    &&TARGET_RERAISE,
    &&TARGET_RESUME,
    &&TARGET_RETURN_CONST,
    &&TARGET_SEND,
    &&TARGET_SEND_GEN,
    &&TARGET_SET_ADD,
    &&TARGET_SET_FUNCTION_ATTRIBUTE,
    &&TARGET_SET_UPDATE,
    &&TARGET_STORE_ATTR,
    &&TARGET_STORE_ATTR_WITH_HINT,
    &&TARGET_STORE_DEREF,
    &&TARGET_STORE_FAST,
    &&TARGET_STORE_FAST_LOAD_FAST,
    &&TARGET_STORE_FAST_STORE_FAST,
    &&TARGET_STORE_GLOBAL,
    &&TARGET_STORE_NAME,
    &&TARGET_SWAP,
    &&TARGET_UNPACK_EX,
    &&TARGET_UNPACK_SEQUENCE,
    &&TARGET_UNPACK_SEQUENCE_LIST,
    &&TARGET_UNPACK_SEQUENCE_TUPLE,
    &&TARGET_UNPACK_SEQUENCE_TWO_TUPLE,
    &&TARGET_YIELD_VALUE,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&_unknown_opcode,
    &&TARGET_INSTRUMENTED_RESUME,
    &&TARGET_INSTRUMENTED_END_FOR,
    &&TARGET_INSTRUMENTED_END_SEND,
    &&TARGET_INSTRUMENTED_RETURN_VALUE,
    &&TARGET_INSTRUMENTED_RETURN_CONST,
    &&TARGET_INSTRUMENTED_YIELD_VALUE,
    &&TARGET_INSTRUMENTED_LOAD_SUPER_ATTR,
    &&TARGET_INSTRUMENTED_FOR_ITER,
    &&TARGET_INSTRUMENTED_CALL,
    &&TARGET_INSTRUMENTED_CALL_FUNCTION_EX,
    &&TARGET_INSTRUMENTED_INSTRUCTION,
    &&TARGET_INSTRUMENTED_JUMP_FORWARD,
    &&TARGET_INSTRUMENTED_JUMP_BACKWARD,
    &&TARGET_INSTRUMENTED_POP_JUMP_IF_TRUE,
    &&TARGET_INSTRUMENTED_POP_JUMP_IF_FALSE,
    &&TARGET_INSTRUMENTED_POP_JUMP_IF_NONE,
    &&TARGET_INSTRUMENTED_POP_JUMP_IF_NOT_NONE,
    &&TARGET_INSTRUMENTED_LINE,
    &&_unknown_opcode};
