# import sqlalchemy as sa
from keywords import *
import sqlparse


class Parser:
    def _leaf_loop(self, k_op, val):
        r_list = []
        for k, v in val.items():
            r = self._parse(k, v)
            r_list.append(r)
        return r_list

    def _bit_op(self, k, v):
        return f""

    def _right_side_op(self, k_op, v):
        k, val = next(iter(v.items()))
        if type(val) == dict:
            r = self._leaf_loop(k_op, v)
            r_list = list(map(lambda x: f"({x})", r))
            # I didnt find it needs op to concat them
            r = " ".join([f"{k_op} {x} " for x in r_list])
        else:
            r = f"{k_op} {result}"
        return r

    def _left_side_op(self, k, v):
        pass

    def _both_sides_op(self, k_op, v):
        k, val = next(iter(v.items()))
        if type(val) == dict:
            r = self._leaf_loop(k_op, v)
            r_list = list(map(lambda x: f"({x})", r))
            r = f" {k_op} ".join(r_list)
        else:
            r = f"{k} {k_op} {val}"
        return r

    def _eq_op(self, k_op, v):
        def map_fuc(x):
            table, columns = x
            return list(map(lambda x: f"{table}.{x}", columns))

        result_list = []
        table_dot_columns = list(map(map_fuc, v.items()))
        # for table, columns in v.items():
        #     table_dot_columns = map(lambda x: f"{table}.{x}", columns)
        #     result_list.extend(table_dot_columns)

        return self._both_sides_op("=", v)

    def _column_op(self, v):
        if v == "":
            return "*"
        result_list = []
        for table, columns in v.items():
            table_dot_columns = map(lambda x: f"{table}.{x}", columns)
            result_list.extend(table_dot_columns)
        return ", ".join(result_list)

    # def _exists_op(self, k_op, json_body)
    #     table_name, where_condition = next(iter(json_body.items()))
    #     list_of_string = []
    #     for k, v in where_condition.items():
    #         cond = self._parse(k, v)
    #         list_of_string.append(cond)
    #     return f'{table_name} WHERE {" ".join(list_of_string)}'

    def _from_op(self, json_body):
        table_name, where_condition = next(iter(json_body.items()))
        list_of_string = []
        for k, v in where_condition.items():
            cond = self._parse(k, v)
            list_of_string.append(cond)
        return f'{table_name} WHERE {" ".join(list_of_string)}'

    def _join_op(self, json_body):
        if json_body == "":
            return ""
        to_join_table, on_condition = next(iter(json_body.items()))
        list_of_string = []
        for k, v in on_condition.items():
            cond = self._parse(k, v)
            list_of_string.append(cond)
        on_string = " ".join(list_of_string)
        return f"JOIN {to_join_table} ON {on_string}"

    def _select_op(self, k_op, json_body):
        cols = self._column_op(json_body.get("@column", ""))
        from_body = self._from_op(json_body.get("FROM", ""))
        join_body = self._join_op(json_body.get("JOIN", ""))

        dml_string = f"SELECT {cols} FROM {from_body}"
        return dml_string

    def _parse(self, k, v):
        if k in BOTH_SIDES_OP:
            return self._both_sides_op(k, v)
        elif k in RIGHT_SIDE_OP:
            return self._right_side_op(k, v)
        elif k in RESERVED_METHOD_WORDS:
            attr = f"_{k.lower()}_op"
            return getattr(self, attr)(k, v)
        #     attr = '_{0}_op'.format(key)
        #     if hasattr(self, attr):
        #         method = getattr(self, attr)
        #         return method(value)

    def parse(self, json_body):
        result_list = []
        for k, v in json_body.items():
            if k in RESERVED_METHOD_WORDS:
                result_json = self._parse(k, v)
            elif k.endswith("[]"):
                result = self.parse(v)
                result_json = {k[:-2]: result}
            else:
                raise ValueError("value error")
                # self._parse(k, v)
            print(result_json)
            result_list.append(result_json)
        return result_json
