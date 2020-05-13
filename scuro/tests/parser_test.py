from scuro.sql_parser import PGSQLParser

test_json = """{"SELECT": {"FROM": {"User": {"=": {"id": 82001}}}}}"""
test2 = {
    "PASS":[{"SELECT": {"FROM": {"User": {"=": {"id": 82001}}}}},
            {"SELECT": {
                "FROM": {"Comment": {"OR": {"=": {"momentId": 234}, "=": {"userID": 343}}}}
            }}],
    "Dummy[]": {
        "SELECT": {
            "@COL": {"Moment": ["id", "date"]},
            "FROM": {
                "Moment": {
                    "OR": {
                        "<>": {"id": 410},
                        "AND": {
                            "NOT IN": {"id": (420, 500)},
                            "OR": {
                                "=": {"id": 234},
                                "IN": {"date": ("2017-02-01", "2019-05-01")}
                            }
                        }
                    },
                    "EXISTS": {
                        "SELECT": {
                            "FROM": {
                                "Comment": {
                                    "=": [
                                        {"DOT_CONCAT": ["Moment", "id"]},
                                        {"DOT_CONCAT": ["Comment", "momentId"]}
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "PASS": [
                {"JOIN": {
                    "table1": {
                        "=": [
                            {"DOT_CONCAT": ["Moment", "id"]},
                            {"DOT_CONCAT": ["table1", "MomentId"]}
                        ]
                    }
                }},
                {"JOIN": {
                    "table2": {
                        "=": [
                            {"DOT_CONCAT": ["Moment", "id"]},
                            {"DOT_CONCAT": ["table2", "MomentId"]}
                        ]
                    }
                }}
            ]
        },
        "Sub_List[]": {
            "PASS": [{"SELECT": {"FROM": {"User": {"=": {"id": 82001}}}}},
            {"SELECT": {
                "FROM": {
                    "Comment": {"OR": {"=": {"momentId": 234}, "=": {"userID": 343}}}
                }
            }}]
        }
    }
}

test3 = """
{
  "SELECT":{
    "FROM":{
      "User":{
        "=":{
          "id":82001
        }
      }
    }
  },
  "SELECT":{
    "FROM":{
      "Comment":{
        "OR":{
          "=":{
            "momentId":234
          },
          "=":{
            "userID":343
          }
        }
      }
    }
  },
  "Dummy[]":{
    "SELECT":{
      "@COL":{
        "Moment":[
          "id",
          "date"
        ]
      },
      "FROM":{
        "Moment":{
          "OR":{
            "<>":{
              "id":410
            },
            "AND":{
              "NOT IN":{
                "id":[
                  420,
                  500
                ]
              },
              "OR":{
                "=":{
                  "id":234
                },
                "IN":{
                  "date":[
                    "2017-02-01",
                    "2019-05-01"
                  ]
                }
              }
            }
          },
          "EXISTS":{
            "SELECT":{
              "FROM":{
                "Comment":{
                  "=":{
                    "DOT_CONCAT":[
                      "Moment",
                      "id"
                    ],
                    "DOT_CONCAT":[
                      "Comment",
                      "momentId"
                    ]
                  }
                }
              }
            }
          }
        }
      },
      "JOIN":{
        "table1":{
          "=":{
            "DOT_CONCAT":[
              "Moment",
              "id"
            ],
            "DOT_CONCAT":[
              "table1",
              "MomentId"
            ]
          }
        }
      }
    },
    "Sub_List[]":{
      "SELECT":{
        "FROM":{
          "User":{
            "=":{
              "id":82001
            }
          }
        }
      },
      "SELECT":{
        "FROM":{
          "Comment":{
            "OR":{
              "=":{
                "momentId":234
              },
              "=":{
                "userID":343
              }
            }
          }
        }
      }
    }
  }
}
"""
import orjson

t = orjson.loads(test3)

p = PGSQLParser()
result_list = p.parse(test2)
import pprint

pprint.pprint(result_list)
