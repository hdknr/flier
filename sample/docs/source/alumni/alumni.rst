====================================
Web名簿システム
====================================


.. contents::
    :local:

.. _alumni.status:

会員区分
=============

会員区分コード
-----------------

- :ref:`alumni.models.AlumnusImport` の status フィールドに指定される値

年度会支援データ
----------------

- :ref:`communities.models.ImportMember` の status フィールドに指定される値

.. include:: include.alumni.status.rst

一括更新
==============

- CSVファイルをインポートテーブルにアップロード
- エラーチェック
- インポートテーブルを管理者用名簿に更新or追加
- インポートテーブルを一般会員名簿に更新or追加

インポート
--------------

件数確認
---------------

- 件数の表示 1) 追加 2)更新 3)削除 

エラーチェック
-----------------

更新
-----

管理者用名簿更新
^^^^^^^^^^^^^^^^^^^

- フィールドの先頭が、"*"のレコードは"*"を除いて表示させます。

一般会員名簿更新
^^^^^^^^^^^^^^^^^^^

- フィールドの先頭が、"*"のレコードは"*"のみで更新します。

追加
-------

管理者用名簿追加
^^^^^^^^^^^^^^^^^^^

- 管理者名簿に存在しないレコードでインポートテーブルに存在するレコードは追加対象です。
- フィールドデータ処理は 管理者用名簿更新と同じ処理を行います。

一般会員名簿追加
^^^^^^^^^^^^^^^^^^^

- 一般会員名簿に存在しないレコードでインポートテーブルに存在するレコードは追加対象です。
- Web公開指定フィールドに"*"が指定されてるレコードは 一般会員名簿更新テーブルに追加しません
- フィールドデータ処理は 一般会員名簿更新と同じ処理を行います。

削除
--------

管理者用名簿削除
^^^^^^^^^^^^^^^^^^^

- インポートテーブルに存在しないレコードで管理者用名簿に存在するレコードは削除対象です。

一般会員名簿削除
^^^^^^^^^^^^^^^^^^^

- インポートテーブルに存在しないレコードで一般会員名簿に存在するレコードは削除対象です。
- インポートテーブでのWeb公開していフィールドに"*"がしているされているレコードは削除対象です。

表示
==============

管理者検索
-------------

- Web公開指定が "\*” (非公開)の会員はわかるように色を変えます。
- 表示フィールドと同等の一般会員用名簿のフィールドが "*"の場合、わかるように色を変えます。


旧システムからの移行
======================

管理者名簿:

.. code-block:: bash

    $ ../manage.py jsupgrade alumnus master

一般名簿:

.. code-block:: bash

    $ ../manage.py jsupgrade alumnus public

実装ステータス
===============

名簿更新
---------

- 現在はデータ処理の一部を実装。UIは未実装。
- CSVのインポート、 インポート後の処理判定、実際の更新、追加、削除
- インポート時に :ref:`alumni.models.AlumnusHistory` でデータをバックアップ(インポートデータ+削除予定データ)
- バックアップする削除予定データは :ref:`alumni.models.AlumnusMaster` と :ref:`alumni.models.AlumnusPublic`  
  のフィールドデータをマージする。
-  :ref:`alumni.models.AlumnusHistory` からいざという時に戻せるようにする。
- インポート処理には名称を指定できるようにしていて、あとでわかるようになっている。

.. todo::
    - 追加時の新規ユーザー登録、削除時のユーザー無効処理は未実装。
    - 履歴からのデータの戻し。
    - ジョブキューを実装し、バックグラウンドで処理できるようにする。(ブラウザセッションが死んだ時異常終了しないように)

UI
-----

.. todo::
    - 一般検索を実装する
    - 管理者検索を実装する
    - メール送信機能を実装する
