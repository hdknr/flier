
.. _communities.models.Community.status:

ステータス(status)フィールド
------------------------------

以下の状態になります:

.. list-table::

    *   - データ
        - 意味
        - 一覧表示 
        - その他の機能

    *   - 0
        - 活動中
        - 一覧表示される
        - 機能を使うことができる(幹事がいるので)
           
    *   - 1
        - 休止中
        - 一覧表示される。

          つまり存在だけはユーザーが目にすることができる。
        - 機能を使うことができない(幹事がいないので)
           
    *   - 2
        - 無効
        - 表示されない
        - 機能を使うことができない
