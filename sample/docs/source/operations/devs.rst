=====
開発
=====


MySQL
=========

trauncate table
------------------------


.. code-block:: mysql

    mysql> SET FOREIGN_KEY_CHECKS = 0; 
    Query OK, 0 rows affected (0.00 sec)
    
    mysql> truncate table accounts_profile;
    Query OK, 0 rows affected (0.01 sec)
    
    mysql> SET FOREIGN_KEY_CHECKS = 1;
    Query OK, 0 rows affected (0.00 sec)
