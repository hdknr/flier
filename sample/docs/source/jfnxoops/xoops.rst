========================
Xoopsシステムからの移行
========================

.. contents::
    :local:

移行準備
=============

移行実行
=============

XOOPSユーザーの移行
----------------------------

名簿の移行
------------

管理者検索データ

.. code-block:: bash

    $ python jsupgrade alumnus master


.. _jfnxoops.tasks:

タスク仕様
=============


.. automodule:: jfnxoops.tasks
    :members:
    :private-members:
    :special-members:

.. _jfnxoops.commands:

管理コマンド仕様
==========================

.. autoclass:: jfnxoops.management.commands.jsupgrade.Command
    :members:
    :private-members:
    :special-members:

