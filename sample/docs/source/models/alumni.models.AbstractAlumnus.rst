旧システムとの対応
------------------------

.. list-table::  名簿システムのデータフィールド一覧

    *    -  名称
         -  旧フィールド名
         -  新フィールド名
         -  タイプ

    *    -  ID
         -  
         -  id
         -  integer AUTO_INCREMENT

    *    -  更新区分
         -  WKKUBN
         -  update_type
         -  varchar(2)

    *    -  :ref:`会員区分 <alumni.status>`
         -  WKACCD
         -  status
         -  varchar(2)

    *    -  会員コード
         -  WKA6CD
         -  js_number
         -  varchar(12)

    *    -  生年月日
         -  WKAFTM
         -  birthday
         -  varchar(16)

    *    -  学部コード
         -  WKAECD
         -  dept_code
         -  varchar(4)

    *    -  卒業年
         -  WKSOTU
         -  finish_year
         -  varchar(8)

    *    -  入学年
         -  WKNYU
         -  entrance_year
         -  varchar(8)

    *    -  クラス会
         -  WKCLAS
         -  class_reunion
         -  varchar(10)

    *    -  各会1
         -  WKAICD
         -  party_code_1
         -  varchar(6)

    *    -  各会2
         -  WKFHCD
         -  party_code_2
         -  varchar(6)

    *    -  各会3
         -  WKA9CD
         -  party_code_3
         -  varchar(6)

    *    -  各会4
         -  WKB8CD
         -  party_code_4
         -  varchar(6)

    *    -  各会5
         -  WKCCCD
         -  party_code_5
         -  varchar(6)

    *    -  各会6
         -  WKCPCD
         -  party_code_6
         -  varchar(6)

    *    -  各会7
         -  WKDXCD
         -  party_code_7
         -  varchar(6)

    *    -  各会8
         -  WKDKCD
         -  party_code_8
         -  varchar(6)

    *    -  各会9
         -  WKELCD
         -  party_code_9
         -  varchar(6)

    *    -  各会10
         -  WKE0CD
         -  party_code_10
         -  varchar(6)

    *    -  指名
         -  AXAUIG
         -  full_name
         -  varchar(44)

    *    -  指名カナ
         -  AXAQTX
         -  full_name_kana
         -  varchar(44)

    *    -  旧姓
         -  AXAVIG
         -  former_name
         -  varchar(44)

    *    -  卒年号1
         -  AIAEIG
         -  finish_era_name_1
         -  varchar(12)

    *    -  卒年度1
         -  AXB9CD
         -  finish_era_year_1
         -  varchar(4)

    *    -  卒学部コード1
         -  AXAECD
         -  finish_dept_code_1
         -  varchar(4)

    *    -  卒学部名1
         -  AXAFTX
         -  finish_dept_name_1
         -  varchar(12)

    *    -  卒業年1
         -  SOTU01
         -  finish_year_1
         -  varchar(8)

    *    -  Finish Era Name 2
         -  AIAEIG01
         -  finish_era_name_2
         -  varchar(12)

    *    -  Finish Era Year 2
         -  AXBBCD
         -  finish_era_year_2
         -  varchar(4)

    *    -  Finish Dept Code 2
         -  AXBDCD
         -  finish_dept_code_2
         -  varchar(4)

    *    -  Finish Dept Name 2
         -  AXBCIG
         -  finish_dept_name_2
         -  varchar(12)

    *    -  Finish Year 2
         -  SOTU02
         -  finish_year_2
         -  varchar(8)

    *    -  Finish Era Name 3
         -  AIAEIG02
         -  finish_era_name_3
         -  varchar(12)

    *    -  Finish Era Year 3
         -  AXBECD
         -  finish_era_year_3
         -  varchar(4)

    *    -  Finish Dept Code 3
         -  AXBGCD
         -  finish_dept_code_3
         -  varchar(4)

    *    -  Finish Dept Name 3
         -  AXBEIG
         -  finish_dept_name_3
         -  varchar(12)

    *    -  Finish Year 3
         -  SOTU03
         -  finish_year_3
         -  varchar(8)

    *    -  勤務先名カナ
         -  AUAMTX
         -  office_name_kana
         -  varchar(124)

    *    -  勤務先名
         -  AXAOIG
         -  office_name
         -  varchar(156)

    *    -  役職
         -  AXADIG
         -  office_title
         -  varchar(36)

    *    -  部署
         -  AXAXIG
         -  office_division
         -  varchar(156)

    *    -  勤務先郵便番号
         -  AXAOCD
         -  offie_zip
         -  varchar(20)

    *    -  勤務先住所
         -  KINMUADR
         -  office_address
         -  varchar(252)

    *    -  勤務先電話番号
         -  AXBHCD
         -  office_phone
         -  varchar(40)

    *    -  在籍カナ名称
         -  AUAMTX01
         -  office_enrollment_kana
         -  varchar(124)

    *    -  在籍名称
         -  AUAOIG
         -  office_enrollment
         -  varchar(156)

    *    -  自宅郵便番号
         -  AXBMCD
         -  home_zip
         -  varchar(20)

    *    -  自宅重祚
         -  JITAKUADR
         -  home_address
         -  varchar(252)

    *    -  自宅電話番号
         -  AXATTX
         -  home_phone
         -  varchar(40)

    *    -  ゼミ1
         -  AXAAIG
         -  seminar_1
         -  varchar(52)

    *    -  ゼミ2
         -  AXBJIG
         -  seminar_2
         -  varchar(52)

    *    -  サークル1
         -  AXACIG
         -  circle_1
         -  varchar(52)

    *    -  サークル2
         -  AXBKIG
         -  circle_2
         -  varchar(52)

    *    -  会費課金
         -  KAKIN
         -  kakin
         -  varchar(2)

    *    -  Home Fax
         -  WKHFNO
         -  home_fax
         -  varchar(40)

    *    -  Email PC
         -  WKPCML
         -  email_pc
         -  varchar(108)

    *    -  Email Mobile
         -  WKMBML
         -  email_mobile
         -  varchar(108)

    *    -  Office Fax
         -  WKOFNO
         -  office_fax
         -  varchar(40)

    *    -  Office Email
         -  WKOFML
         -  email_office
         -  varchar(108)

    *    -  WEB掲載区分
         -  DELFLG
         -  delflg
         -  varchar(1)

    *    -  md5
         -  MD5
         -  md5
         -  varchar(128)

    *    -  作成時刻
         -  
         -  created_at
         -  datetime

    *    -  更新時刻
         -  
         -  updated_at
         -  datetime

WEB掲載区分(削除フラグ)
---------------------------------------------

.. code-block:: php

        // - 全非表示データはDELFLGに"1"を付設、
        // - 部分非表示のデータには"2"を
        // - それ以外は"0"を付設
        if($row[59] == '*') {
          $r["DELFLG"] = '1' ;
        } elseif (
            substr($row[37],0,1) == '*' || 
            substr($row[38],0,1) == '*' || 
            substr($row[39],0,1) == '*' || 
            substr($row[40],0,1) == '*' || 
            substr($row[41],0,1) == '*' || 
            substr($row[42],0,1) == '*' || 
            substr($row[43],0,1) == '*' || 
            substr($row[44],0,1) == '*' || 
            substr($row[45],0,1) == '*' || 
            substr($row[46],0,1) == '*' || 
            substr($row[47],0,1) == '*' || 
            substr($row[48],0,1) == '*' || 
            substr($row[54],0,1) == '*' || 
            substr($row[55],0,1) == '*' || 
            substr($row[56],0,1) == '*' || 
            substr($row[57],0,1) == '*' ||
            substr($row[58],0,1) == '*') {
          $r["DELFLG"] = '2' ;
        } else {
          $r["DELFLG"] = '0' ;
        } 
