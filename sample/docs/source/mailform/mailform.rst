====================================
旧問い合わせシステム
====================================

.. contents::
    :local:


データベース
============

.. list-table::

    *   - データベース名
        - mailform

    *   - ユーザー
        - www-data

    *   - パスワード
        - mailform

::

    $ psql -h localhost -p 5432 -U www-data -W mailform
    ユーザ www-data のパスワード: mailform
    psql (8.4.22lts2)
    "help" でヘルプを表示します.

    mailform=>

テーブル
----------

.. code-block:: psql

    mailform=> \dt
                リレーションの一覧
     スキーマ |  名前  |      ?      | 所有? 
    --------------+----------+--------------+----------
     public       | ad_user  | テーブル | postgres
     public       | bansan   | テーブル | postgres
     public       | gyouji   | テーブル | postgres
     public       | idou     | テーブル | postgres
     public       | jukou    | テーブル | postgres
     public       | kougi    | テーブル | postgres
     public       | meibo    | テーブル | postgres
     public       | nyukai   | テーブル | postgres
     public       | toiawase | テーブル | postgres
    (9 行)


システムユーザー
------------------------------

.. code-block:: postgresql


    CREATE TABLE ad_user (
        id character varying(20),
        pass character varying(20),
        allt integer,
        nyukai integer,
        idou integer,
        meibo integer,
        bansan integer,
        gyouji integer,
        jyukou integer,
        kougi integer,
        toiawase integer
    );

晩餐(bansan)
---------------------------

.. code-block:: postgresql

    CREATE TABLE bansan (
        kaisai character varying(15),
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        mail character varying(150),
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    

行事(gyouji)
---------------------------

.. code-block:: postgresql

    CREATE TABLE gyouji (
        kaisai character varying(15),
        gyouji character varying(160),
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        mail character varying(150),
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    
    
異動・変更(idou)
---------------------------

.. code-block:: postgresql

    CREATE TABLE idou (
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        cname character varying(100),
        cnameflg integer,
        ctel character varying(20),
        ctelflg integer,
        caddnum character varying(10),
        caddnumflg integer,
        cshozoku character varying(100),
        cshozokuflg integer,
        cadd character varying(160),
        caddflg integer,
        czaiseki character varying(100),
        czaisekiflg integer,
        tel character varying(20),
        telflg integer,
        addnum character varying(10),
        addnumflg integer,
        add character varying(160),
        addflg integer,
        bikou text,
        cfax character varying(20),
        cfaxflg integer,
        cmail character varying(150),
        cmailflg integer,
        fax character varying(20),
        faxflg integer,
        mail character varying(150),
        mailflg integer,
        mmail character varying(150),
        mmailflg integer,
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );

受講(jukou)
---------------------------

.. code-block:: psql
    
    CREATE TABLE jukou (
        kaiki character varying(10),
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        mail character varying(150),
        douki text,
        bikou text,
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );

講義(kougi)
---------------------------

.. code-block:: postgresql
    
    CREATE TABLE kougi (
        kaiki character varying(10),
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        mail character varying(150),
        souhu character varying(20),
        bikou text,
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    

名簿(meibo)
---------------------------

.. code-block:: postgresql
    
    CREATE TABLE meibo (
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        mail character varying(150),
        souhu character varying(20),
        meibo character varying(60),
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    

入会申込(nyukai)
---------------------------

.. code-block:: postgresql

    CREATE TABLE nyukai (
        namef character varying(50),
        name character varying(50),
        sotunen character varying(10),
        gakubu character varying(50),
        addnum character varying(10),
        add character varying(160),
        tel character varying(20),
        mail character varying(150),
        bikou text,
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    

問合せ(toiawase)
---------------------------

.. code-block:: psql

    CREATE TABLE toiawase (
        namef character varying(50),
        name character varying(50),
        num character varying(10),
        sotunen character varying(10),
        gakubu character varying(50),
        addnum character varying(10),
        add character varying(160),
        tel character varying(20),
        mail character varying(150),
        toiawase text,
        id integer NOT NULL,
        day timestamp without time zone,
        delflg character varying(10)
    );
    

登録
==========

- ログインユーザーであればフォームの個人情報が自動的に埋められます

通知メール
--------------

登録されるとメールが２通送られます

- 事務局メール
- 会員向け自動返信メール

事務局メール
^^^^^^^^^^^^^^^^^^^

修正

- 内容に変更がある場合は、項目毎に【変更あり】と表示

掲載/非掲載

- 掲載する/掲載しないのみの変更は、【＊変更あり】で行う
- 内容も掲載/非掲載も変更した場合　【変更あり】

空欄

- 空欄に変更した場合は、【空欄に変更】
- 空欄に変更して、かつ掲載/非掲載を変えた場合【空欄に変更】【＊変更あり】
- もともと空欄で、掲載/非掲載のみ変えた場合【＊変更あり】

.. literalinclude:: mailform.admin.txt

会員向け自動返信メール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: mailform.user.txt

スキーマ
===========

.. literalinclude:: mailform.schema.sql
