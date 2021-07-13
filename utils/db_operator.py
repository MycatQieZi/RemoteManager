from functools import wraps
from conf.config import ConfigManager
from settings.settings_manager import SettingsManager
from misc.decorators import singleton
from utils.my_logger import logger

import sqlite3, traceback, uuid, logging

def transaction_driver(enabled_transaction, fn_action, logger, message):
    if(enabled_transaction):
        if(logger):
            logger.debug(message)
        fn_action()

def with_connection_and_transaction(transaction=False):
    """
    transaction==False: sqlite auto-control transaction
        using autocommit; when executing each statement, takes effect immediately

    transaction==True: manually control transaction
        sqlite3 automatically puts BEGIN statement before execution, need to manually
        COMMIT or ROLLBACK 
    """
    def wrapper(fn):
        @wraps(fn)
        def execution(self, *args, **kwargs):
            connection = sqlite3.connect(self.sqlite_path, timeout=10.0, isolation_level=None)   
            conn_id = uuid.uuid4()
            self.conn_pool[conn_id] = connection
            cursor = connection.cursor()
            try:
                result = fn(self, cursor, *args, **kwargs)
            except Exception:
                transaction_driver(transaction, connection.rollback, self.logger, "手动回滚事务, 原因:\n"+traceback.format_exc())
                raise
            else:
                transaction_driver(transaction, connection.commit, self.logger, "手动提交事务")
                return result
            finally:
                connection.close()
                self.conn_pool.pop(conn_id, None)
        return execution
    return wrapper

@singleton
@logger
class DBOperator():
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.config_manager = ConfigManager()
        self.sqlite_path = "%s\\%s" %(self.settings_manager.get_sqlite_db_path(), self.config_manager.get_config_item_by_mapping("dbfileName"))
        self.conn_pool = {}

    @with_connection_and_transaction()    
    def get_all_ongoing_task_ids(self, cursor, *_, **__):
        statement = "SELECT id FROM `task` WHERE `status`=1 OR `status`=2;"
        cursor.execute(statement)
        query_result = cursor.fetchall()
        task_ids = list(map(lambda tuple: tuple[0], query_result))
        self.debug("task_ids: %s", str(task_ids))
        return task_ids
    
    @with_connection_and_transaction(transaction=True)
    def execute_sql_file(self, cursor, *args, **_):
        sql_as_string = args[0]
        cursor.executescript(sql_as_string)
        

    def close_all_connections(self):
        for _, connection in self.conn_pool.items():
            try:
                connection.close()
            except:
                self.logger.error("Cannot close connection: %s", traceback.format_exc())
                continue