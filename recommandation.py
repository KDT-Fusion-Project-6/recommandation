import item_simirarity as ism
import user_simirarity as usm
from import_data import database

condition = {}
db = database('localhost', 'root', 'jong1003', 'codi')

db.select_where_with_condition(condition)
