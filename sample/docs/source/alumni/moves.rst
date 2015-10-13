===========
異動申請
===========

.. contents::
    :local:

.. todo::
    - 問い合わせは如水会登録個人情報(AS400用)の異動情報のみを移行する


旧異動フォーム(mailform/idou)
===================================

.. list-table::
    :header-rows: 1
    
    *   - 項目名
        - データ型
        - 桁数
        - 項目名ラベル  
        - 表示ブロック    
        - 入力形式    
        - 必須    
        - 入力ルール  
        - エラーメッセージ1   
        - エラーメッセージ2   
        - エラーメッセージ3
        
    *   - namef 
        - varchar
        - 50
        - 氏名フリガナ      
        - (一般)
        - テキスト
        - 
        - カタカナのみ 
        - 
        - 
        - 

    *   - name 
        - varchar
        - 50
        - 氏名      
        - (一般)
        - テキスト    
        - 必須
        - 
        - 
        - 
        - 

    *   - num 
        - varchar
        - 10
        - 会員番号
        - (一般) 
        - 半角
        - 必須
        - 数字、6ケタ　※全角入力の場合は、半角に変換    
        - 会員番号を数字で入力してください    
        - 会員番号の文字数が長すぎます
        - 

    *   - sotunen 
        - varchar
        - 10
        - 卒年  
        - (一般)  
        - プルダウン（昭和/平成）＋年     
        - 
        - 年→半角2ケタの数字  "
        - （和暦選択がない場合）卒年を正しく入力してください"   "
        - （年に文字を入力した場合） 卒年を正しく入力してください。" "
        - （卒年3ケタ以上） 卒年の文字数が長すぎます"

    *   - gakubu 
        - varchar
        - 50
        - 学部  
        - (一般)  
        - テキスト
        - 
        - 
        - 
        - 
        - 

    *   - cname 
        - varchar
        - 100
        - 名称  
        - 勤務先  
        - テキスト
        - 
        - 
        - 
        - 
        - 

    *   - cnameflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - ctel 
        - varchar
        - 20
        - 電話  
        - 勤務先  
        - 半角        
        -
        - nnn-nnnn-nnnn (ハイフン必須の数字列)
        - 勤務先電話番号を正しい形式で入力してください
        -
        -

    *   - ctelflg 
        - integer
        -
        -
        -
        -
        -
        -
        -
        -
        -

    *   - caddnum 
        - varchar
        - 10
        - 郵便番号  
        - 勤務先  
        - 半角        
        -
        - nnnnnnnnnn (ハイフンなしの10桁数字列)
        - 10ケタまで" 勤務先郵便番号を数字のみで入力してください  
        - 勤務先郵便番号の文字数が長すぎます
        -

    *   - caddnumflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - cshozoku 
        - varchar
        - 100
        - 所属・役職    
        - 勤務先  
        - テキスト
        -
        -
        -
        -
        -

    *   - cshozokuflg 
        - integer
        -
        -
        -
        -
        -
        -
        -
        -
        -

    *   - cadd 
        - varchar
        - 160
        - 所在地    
        - 勤務先  
        - テキスト
        - 
        - 
        - 
        - 
        - 

    *   - caddflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - czaiseki 
        - varchar
        - 100
        - 在籍（出向元）    
        - 勤務先  
        - テキスト
        -
        -
        -
        -
        -

    *   - czaisekiflg 
        - integer
        -
        -
        -
        -
        -
        -
        -
        -
        -

    *   - tel 
        - varchar
        - 20
        - 電話    
        - 自宅    
        - 半角
        -
        - nnn-nnnn-nnnn(ハイフン必須の数字列)
        - 自宅電話番号を正しい形式で入力してください
        -
        -

    *   - telflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - addnum 
        - varchar
        - 10
        - 郵便番号   
        - 自宅    
        - 半角
        -
        - nnnnnnnnnn(ハイフンなし数字列)
        - 自宅郵便番号を数字のみで入力してください    
        - 自宅郵便番号の文字数が長すぎます
        - 

    *   - addnumflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - add 
        - varchar
        - 160
        - 住所   
        - 自宅    
        - テキスト
        -
        -
        -
        -
        -

    *   - addflg 
        - integer
        -
        -
        -
        -
        -
        -
        -
        -
        -

    *   - bikou 
        - text
        - 
        - 備考        
        - 
        - テキスト
        -
        -
        -
        -
        -


    *   - cmail 
        - varchar
        - 150
        - E-mail    
        - 勤務先  
        - 半角    
        - cmail/mailどちらか必須
        - メールアドレス 
        - E-mailを正しく入力してください
        - 
        - 

    *   - cmailflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - mail 
        - varchar
        - 150
        - E-mail    
        - 勤務先  
        - 半角    
        - cmail/mailどちらか必須
        - メールアドレス 
        - E-mailを正しく入力してください
        - 
        - 

    *   - mailflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - mmail 
        - varchar
        - 150
        - 携帯E-mail    
        - 自宅    
        - 半角
        - 
        - 
        - 
        - 
        - 

    *   - mmailflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - delflag
        - integer
        - 
        - 
        - 
        - 
        - 
        - 1: 全非表示, 2: 部分非表示, 0: それ以外 
        - 
        - 
        - 


.. list-table:: 今後使わないデータ項目
    :header-rows: 1

    *   - 項目名
        - データ型
        - 桁数
        - 項目名ラベル  
        - 表示ブロック    
        - 入力形式    
        - 必須    
        - 入力ルール  
        - エラーメッセージ1   
        - エラーメッセージ2   
        - エラーメッセージ3
        
    *   - cfax 
        - varchar
        - 20
        - fax（使用なし）   
        - 勤務先
        - 
        - 
        - 
        - 
        - 
        - 

    *   - cfaxflg 
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - fax 
        - varchar
        - 20
        - fax（使用なし）
        - 
        - 
        - 
        - 
        - 
        - 
        - 

    *   - faxflg    
        - integer
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 
        - 

