from scuro.sql_parser.pg_keywords import *


class PGSQLParser:
    def _leaf_loop(self, val, k_op):
        r_list = []
        for k, v in val.items():
            r = self._parse(v, k)
            r_list.append(r)
        return r_list

    def _pass_op(self, containers_list, k=None):
        result_list = []
        for json_body in containers_list:
            result_list.extend(self.parse(json_body))
        return result_list

    def _bit_op(self, v, k):
        return f""

    def _right_side_op(self, v, k_op):
        k, val = next(iter(v.items()))
        if type(val) == dict:
            r = self._leaf_loop(v, k_op)
            r_list = list(map(lambda x: f"({x})", r))
            # I didnt find it needs op to || them
            r = " ".join([f"{k_op} {x} " for x in r_list])
        else:
            r = f"{k_op} {val}"
        return r

    def _left_side_op(self, v, k):
        pass

    def _both_sides_op(self, v, k_op):
        """
        It can have three situations:
        1. v is a list of dict:
            This happens when there are multiple same operators in the dict, but dict/json can't have
            duplicated keys. So we wrap them with a list. We treat each dict in list as a independent expression.
            Parse the dicts in the list iteratively, return a list of parsed expressions
        2. v is a dict:
            When there are no duplicate keys.
        3. v is a single value
            We are at the end of the recursion.
        Parameters
        ----------
        k_op:
            Operator from the above level, used to concat both sides of string
        v

        Returns
        -------

        """
        if type(v) == list:
            result_list = self._pass_op(v)
            r = f' {k_op} '.join(result_list)
            return r

        k, val = next(iter(v.items()))
        if type(val) == dict:
            r = self._leaf_loop(v, k_op)
            r_list = list(map(lambda x: f"({x})", r))
            r = f" {k_op} ".join(r_list)
        else:
            r = f"{k} {k_op} {val}"
        return r

    def _dot_concat_op(self, v, k_op=None):
        return f"{v[0]}.{v[1]}"

    def _column_op(self, v):
        if v == "":
            return "*"
        result_list = []
        for table, columns in v.items():
            table_dot_columns = map(lambda x: f"{table}.{x}", columns)
            result_list.extend(table_dot_columns)
        return ", ".join(result_list)

    # def _exists_op(self, json_body, k_op)
    #     table_name, where_condition = next(iter(json_body.items()))
    #     list_of_string = []
    #     for k, v in where_condition.items():
    #         cond = self._parse(v, k)
    #         list_of_string.append(cond)
    #     return f'{table_name} WHERE {" ".join(list_of_string)}'

    def _from_op(self, json_body):
        table_name, where_condition = next(iter(json_body.items()))
        list_of_string = []
        for k, v in where_condition.items():
            cond = self._parse(v, k)
            list_of_string.append(cond)
        return f'{table_name} WHERE {" ".join(list_of_string)}'

    def _join_op(self, json_body, k=None):
        if json_body == "":
            return ""
        elif type(json_body) == list:
            list_of_string = self._pass_op(json_body)
        else:
            to_join_table, on_condition = next(iter(json_body.items()))
            list_of_string = []
            for k, v in on_condition.items():
                cond = self._parse(v, k)
                list_of_string.append(cond)
        on_string = " ".join(list_of_string)
        return f"JOIN {to_join_table} ON {on_string}"

    # def _concat_op(self, v, k_op):

    def _select_op(self, json_body, k_op):
        """
        Its not very accurate to call it select cuz its a container to hold a query
        """
        cols = self._column_op(json_body.get("@column", ""))
        from_body = self._from_op(json_body.get("FROM", ""))
        join_body = self._join_op(json_body.get("JOIN", ""))
        pass_list = self._pass_op(json_body.get("PASS", ""))
        pass_body = " ".join(pass_list)

        dml_string = f"SELECT {cols} FROM {from_body} {join_body} {pass_body}"
        return dml_string

    def _parse(self, v, k):
        if k in BOTH_SIDES_OP:
            return self._both_sides_op(v, k)
        elif k in RIGHT_SIDE_OP:
            return self._right_side_op(v, k)
        elif k in OP_WORDS:
            attr = f"_{k.lower()}_op"
            return getattr(self, attr)(v, k)
        #     attr = '_{0}_op'.format(key)
        #     if hasattr(self, attr):
        #         method = getattr(self, attr)
        #         return method(value)

    def parse(self, json_body):
        result_list = []
        for k, v in json_body.items():
            if k in RESERVED_WORDS:
                result_string = self._parse(v, k)
            elif k.endswith("[]"):
                result = self.parse(v)
                result_string = {k[:-2]: result}
            else:
                raise ValueError("value error")
                # self._parse(v, k)
            # print(result_json)
            result_list.append(result_string)
        return result_list

        # if type(v) ==  dict:
        #     # the value is a json object
        #     if k.endswith('[]'):
        #         # its a array of tables
        #         for table in v:
        #             parse(table)
        #     else:
        #         # its a single table
        #         for col, val in v.items():
        #             if col.endswith('{}'):
        # elif k.endswith('{}'):
