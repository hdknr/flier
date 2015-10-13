====================================
会報システム
====================================

.. contents::
    :local:

.. _bulletins.models.Bulletin:

Bulletin:会報誌
========================

.. autoclass:: bulletins.models.Bulletin
    :members:


.. list-table::

    *    - id
         - ID
         - integer AUTO_INCREMENT
         - 

    *    - code
         - コード
         - varchar(20)
         - 

    *    - filename
         - ファイル名
         - varchar(50)
         - 

    *    - bulletin
         - 会報誌区分
         - integer
         - 

           .. list-table::

               *    - 0
                    - 同窓會會誌
           
               *    - 1
                    - 如水会々報
           

    *    - volume
         - 号
         - integer
         - 

    *    - issued_year
         - 発行年
         - integer
         - 

    *    - issued_month
         - 発行月
         - integer
         - 

    *    - issued_day
         - 発行日
         - integer
         - 

    *    - page_first
         - 開始頁
         - integer
         - 

    *    - page_last
         - 終了頁
         - integer
         - 

    *    - category
         - カテゴリー
         - varchar(100)
         - 

    *    - author
         - 著者
         - varchar(200)
         - 

    *    - job_title
         - 肩書
         - varchar(50)
         - 

    *    - title
         - 名称
         - varchar(200)
         - 

    *    - title_alter
         - 異なりアクセスタイトル
         - varchar(200)
         - 

    *    - created_at
         - 作成時刻
         - datetime
         - 

    *    - updated_at
         - 更新時刻
         - datetime
         - 

.. include:: bulletins.models.Bulletin.rst

.. _bulletins.models.MediaFile:

MediaFile:データファイル
==================================

.. autoclass:: bulletins.models.MediaFile
    :members:


.. list-table::

    *    - id
         - ID
         - integer AUTO_INCREMENT
         - 

    *    - data
         - データファイル
         - varchar(100)
         - 

    *    - mimetype
         - コンテントタイプ
         - varchar(30)
         - 

.. include:: bulletins.models.MediaFile.rst


.. _bulletins.models.er:

ER Diagram
============================

.. image:: bulletins_models_er.png

.. _bulletins.models.er:

ER Diagram
============================

.. image:: bulletins_models_er.png
