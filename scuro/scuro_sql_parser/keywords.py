# from pyparsing import Keyword, MatchFirst
# from moz_sql_parser.debugs import debug


AND = None
AS = None
ASC = None
BETWEEN = None
CASE = None
COLLATE_NOCASE = None
CROSS_JOIN = None
DESC = None
END = None
ELSE = None
FROM = None
FULL_JOIN = None
FULL_OUTER_JOIN = None
GROUP_BY = None
HAVING = None
IN = None
INNER_JOIN = None
IS = None
IS_NOT = None
JOIN = None
LEFT_JOIN = None
LEFT_OUTER_JOIN = None
LIKE = None
LIMIT = None
NOT_BETWEEN = None
NOT_IN = None
NOT_LIKE = None
OFFSET = None
ON = None
OR = None
ORDER_BY = None
RESERVED = None
RIGHT_JOIN = None
RIGHT_OUTER_JOIN = None
SELECT = None
THEN = None
UNION = None
UNION_ALL = None
USING = None
WITH = None
WHEN = None
WHERE = None

RESERVED_METHOD_WORDS = [
    "AND",
    "AS",
    "ASC",
    "BETWEEN",
    "CASE",
    "COLLATE_NOCASE",
    "CROSS_JOIN",
    "DESC",
    "END",
    "ELSE",
    "FROM",
    "FULL_JOIN",
    "FULL_OUTER_JOIN",
    "GROUP_BY",
    "HAVING",
    "IN",
    "INNER_JOIN",
    "IS",
    "IS_NOT",
    "JOIN",
    "LEFT_JOIN",
    "LEFT_OUTER_JOIN",
    "LIKE",
    "LIMIT",
    "NOT_BETWEEN",
    "NOT_IN",
    "NOT_LIKE",
    "OFFSET",
    "ON",
    "OR",
    "ORDER_BY",
    "RESERVED",
    "RIGHT_JOIN",
    "RIGHT_OUTER_JOIN",
    "SELECT",
    "THEN",
    "UNION",
    "UNION_ALL",
    "USING",
    "WITH",
    "WHEN",
    "WHERE",
    # self-defined
    "eq",
]

SCURO_WORDS = ["@column"]

BOTH_SIDES_OP = [
    "||",
    "*",
    "/",
    "%",
    "+",
    "-",
    "&",
    "|",
    "<",
    "<=",
    ">",
    ">=",
    "=",
    "==",
    "!=",
    "<>",
    "IN",
    "NOT IN",
    "IS NOT",
    "IS",
    "NOT LIKE",
    "NOT BETWEEN",
    "OR",
    "AND",
]

RIGHT_SIDE_OP = ["EXISTS"]
