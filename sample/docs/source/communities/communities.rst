==================================================
支部会/年度会支援システム
==================================================

.. contents::
    :local:

役割と概要
=================

事務局
--------

- 支部会年度会の登録/更新を行う(:ref:`communities.communities`)
- 支部会の幹事メンバーの登録/更新を行う。(:ref:`communities.membership.managers`)
- 年度会に関しては一般メンバーの登録更新も行う (:ref:`communities.membership.members`)
- 幹事向けに電子メールを送ることができる (:ref:`communities.mails` )

支部会幹事
------------

- 活動報告の登録更新
- 年間スケジュールの登録更新
- メンバーの登録更新
- 活動報告は、1)一般公開 2)如水会員公開 3)メンバーのみ公開の３つの公開を選択可能
- 如水会カードによる会費徴収を行うことができる
- メンバー向けのメールを送信することができる

所属会員
-------------

- 公開コンテンツを見ることができる
- 公開されたメンバーの個人属性をみることができる
- 自分の個人属性の公開ポリシーを変更できる

システムの機能
================


.. _communities.communities:

コミュニティ管理
------------------------

- 事務局が登録/更新の管理を行います(:ref:`communities.models.Community`)
- 支部会の状態として、1)活動 2)休止 3)無効の３ステートがある(:ref:`communities.models.Community.status` )

.. _communities.membership:

会員管理
------------------------------------------------

- 会員の追加/更新を行うことができます。

.. _communities.membership.file:

一括更新
^^^^^^^^^^^^^^

- 一括更新はExcelファイルのアップロードで行うことができます。
- ファイル形式は「:ref:`communities.models.ImportMember` 」で定義しています。


.. _communities.membership.managers:

幹事
^^^^^^^^^^^^^

- 事務局は幹事の登録更新管理を行うことができます。

.. _communities.membership.members:

一般会員
^^^^^^^^^^^^^^

- 事務局は年度会に関しては一般会員の登録更新管理を行うことができます。
- 各会の幹事は一般会員の登録更新管理を行うことができます。

.. _communities.activities:

Web活動報告
---------------

.. _communities.mails:

同報メール送信
---------------

- 事務局は幹事に対して同報メールを送ることができます。
- 各会の幹事は所属会員に関して同報メールを送ることができます。


.. todo::
    - 送り方に関して詳細を詰める


.. _communities.payments:

会費徴収依頼
---------------


旧システムからの移行
=======================

支援システムのデータを移行します:

.. code-block:: bash

    $ ./manage.py jsupgrade community

$XOOPS_SYSTEM/public_html/modules/jscom/images 以下の写真データを移行します:


.. code-block:: bash

    $ ./manage.py jsupgrade community_photo  ~/projects/jfn/xoops/public_html/modules/jscom/images   

.. todo::
    - すでにコミュニティデータが削除されたと思われる写真ファイルが存在します


その他
=========

.. todo::
    - 会の名称はすべての種別を含めてユニークであるか？ 

      ユニークでないならばインポートデータ形式を変更する必要がある。

    - 役職がある、なしでのみ管理者の権限をコントールし、役職の内容で詳細に業務権限を制御する、ということは考えなくてよいか？
