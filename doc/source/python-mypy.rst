======================================================================
mypy 利用ノート
======================================================================

道具としての |mypy| に関する雑記帳にしたいが、論点が絞れないので Python 型注釈機
能に関しても綴っていく。

.. |conda| replace:: :program:`conda`
.. |mypy| replace:: :program:`mypy`
.. |mypy.ini| replace:: :file:`mypy.ini`
.. |pyproject| replace:: :file:`pyproject.toml`

.. contents:: 章見出し
   :local:

概要
======================================================================

   Mypy is a static type checker for Python.

型チェッカーというのは構文チェッカーの特殊なものであるとひとまず理解しておけばい
い。

   Type checkers help ensure that you're using variables and functions in your
   code correctly. With mypy, add type hints (`PEP 484`_) to your Python
   programs, and mypy will warn you when you use those types incorrectly.

Python 言語仕様には、変数、関数、クラス、等々のコード構成要素に対して、その型を
専用形式で注釈を付けることが可能であるというものがある。実際に型ヒントをコードに
付与するようになると実感できるが、Python コードの可読性が高まるという恩恵をも感
じる。関数の引数リストを見るだけで、実引数の型に関する必要条件がわかるというのは
読み書きにおいて大きい利点だ。Mypy_ はそのように注釈が付いたコードを解析、報告す
る道具の一つだと述べている。

   Python is a dynamic language, so usually you'll only see errors in your code
   when you attempt to run it. Mypy is a static checker, so it finds bugs in
   your programs without even running them!

型注釈付きコードを、それを実際に実行する前に検証することを mypy_ は目的とする。

インストール・更新・アンインストール
======================================================================

複数人で共用するプロジェクトの開発環境に mypy_ をインストールする事例では、その
プロジェクトの定める手順に従え。README や |pyproject| を読めば判明する。

自分が所有する作業用仮想環境にインストールするならば、愛用している仮想環境ツール
がインストールコマンドを実装している場合にはそれを使え。私ならば Miniconda_ であ
るから、例えば次のようにする：

.. sourcecode:: console
   :caption: 現在の conda 仮想環境に mypy をインストールする
   :force:

   $ conda install -c conda-forge mypy

インストール手順の説明は以上だ。Mypy_ の更新、アンインストールの手順は、対応する
条件におけるインストール手順に合致する手順を選べ。例えば |conda| を使っているの
ならば ``conda uninstall mypy`` を走らせる。

.. seealso::

   :doc:`/python-miniconda`
      |conda| の使用法はここに記した。

構成・カスタマイズ
======================================================================

プロジェクトの |pyproject| の専用区間またはファイル |mypy.ini| にオプションを指
定するのが普通の運用と考えられる。

ユーザー設定としてファイル :file:`$XDG_CONFIG_HOME/mypy/config` などにオプション
を指定することも可能だ。プロジェクトのほうの指定ファイルが優先される。他にも既定
パスが設けられているが、私が使うファイルはこの二つしかない（のでそれらしか述べな
い）。

   Some flags support user home directory and environment variable expansion. To
   refer to the user home directory, use ``~`` at the beginning of the path. To
   expand environment variables use ``$VARNAME`` or ``${VARNAME}``.

という便宜が図られているので、ユーザー固有の情報を環境変数の形で記載した
|mypy.ini| をバージョン管理のリモートリポジトリーに安心して置きやすい。

.. sourcecode:: ini
   :caption: |mypy.ini| の例
   :force:

   # Global options
   [mypy]
   # Specifies the location where mypy stores incremental cache info.
   cache_dir = "$XDG_CACHE_HOME/mypy"

   # Suppresses error messages about imports that cannot be resolved.
   ignore_missing_imports = True

   # Enable all optional error checking flags.
   # (n.b. includes check_untyped_defs and disallow_untyped_defs options)
   strict = True

.. admonition:: 利用者ノート

   なるべく ``--strict`` オプションを付けたい。これが有効にするオプションの集合
   は ``mypy --help`` の出力から判断可能。オプションの集合は mypy_ を更新するた
   びに変化する可能性がある。

.. seealso::

   `The mypy configuration file <https://mypy.readthedocs.io/en/stable/config_file.html>`__
      公式文書の解説。
   :doc:`/xdg`
      当ノートはドットファイルの配置方針として XDG Base Directory 仕様を採用して
      いる。

使用方法・コツ
======================================================================

前提として、`mypy documentation`_ の最初の方の記述は体得することとする。

型注釈に関する定型コード
----------------------------------------------------------------------

スクリプトにせよモジュールにせよ、Python ファイルのインポート区画は次のコードを
含む：

.. sourcecode:: python
   :caption: 型検査ブロックコード
   :force:

   from __future__ import annotations
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       # E.g. from typing import Never, Self

この ``if`` ブロックでは型注釈にしか必要でないものをインポートする。

型注釈に関する作法
----------------------------------------------------------------------

Python コードに対する静的解析ツール Ruff_ を併用して、型注釈に関する諸規則をオン
にするとよい。

.. seealso::

   :doc:`./python-ruff` の次の節を見ろ：

   * pyupgrade (UP): UP{013,014}, UP040, UP045.
   * flake8-annotations (ANN)
   * flake8-type-checking (TC)

よく用いる注釈用型
----------------------------------------------------------------------

型注釈で用いる型には、オブジェクトの型ずばりそのものである場合とそうでない場合が
ある。例として、自作関数のある引数の型として ``list[str]`` を想定していても、論
理的には ``Sequence[str]`` や ``Iterable[str]`` などが正しいなどという場合が考え
られる。

モジュール `typing <https://docs.python.org/3/library/typing.html>`__ では次をよ
く用いる：

* ``Any``. 未知の型を意味すると覚えておけ。
* ``Final[]``
* ``Literal[]``, ``LiteralString[]``
* ``Never``, ``NoReturn``
* ``Self``. ただし、メソッドの第一引数を ``self: Self`` と明示的に指示する必要は
  ないことに気をつけろ。

モジュール `collections.abc
<https://docs.python.org/3/library/collections.abc.html>`__ で定義された汎用プロ
トコルは重要だ。リンク先文書の `Collections Abstract Base Classes` 節の表を理解
しろ。特に Inherits from 列が重要だ。例えば ``MutableSequence`` が必要なのに
``Sequence`` と書いたり、逆に ``Sequence`` で十分なのに``MutableSequence`` と書
いするのはダメだと心得ろ。

* ``Callable[]``: e.g. ``Callable[[ArgType0, ArgType1, ...], ReturnType]``
* ``Generator[]``: e.g. ``Generator[YieldType, SendType, ReturnType]``
* ``Iterable[]``: e.g. ``Iterable[YieldType]``
* ``Mapping[]``: e.g. ``Mapping[KeyType, ValueType]``
* ``Sequence[]``: e.g. ``Sequence[ValueType]``

書くべき型がわからないときの対処法
----------------------------------------------------------------------

例えば ``with open(path, "r") as fp: ...`` のようなコードが与えられていて、自分
のコードで ``fp`` を引数に取る関数を定義する必要があるとき、その注釈型をドキュメ
ントをなるべく引かずに知りたいとする。

そのようなときには ``typing.reveal_type(fp)`` をコード中に含ませて |mypy| に解析
させる。すると次のように実際の型を示す：

.. sourcecode:: console
   :caption: ``reveal_type`` 呼び出し例
   :force:

   $ cat reveal_type_test.py
        1  from typing import reveal_type
        2
        3  with open("tmp.txt", "r") as fp:
        4      reveal_type(fp)
        5      ...
   $ mypy --strict reveal_type_test.py
   reveal_type_test.py:4: note: Revealed type is "_io.TextIOWrapper[_io._WrappedBuffer]"
   Success: no issues found in 1 source file

この場合、型注釈としては ``typing.TextIO`` を用いるのが正解となる。なお、この例
では ``open`` の第二引数の値によって ``fp`` の型が変わる。

.. caution::

   ``reveal_type`` 呼び出しが製品コードにあってはならない。

..
   N.b. mypy とは関係ないが：
   Visual Studio Code で適当な Python 拡張をインストールしていてコードを編集する
   のであれば、``reveal_type(fp)`` 内の ``fp`` にマウスカーソルを hover させると
   ポップアップウィンドウに型が示される。

型を |mypy| に教える
----------------------------------------------------------------------

下のコードは BeautifulSoup を用いた処理の断片だ。生の ``column.text`` のままでは
|mypy| はこの型が ``str`` であることが推論できず ``strip`` 呼び出しをエラーとみ
なす。こういう場合には例えば関数 ``typing.cast`` 呼び出しで対象部分をラップする
と上手くいく：

.. sourcecode:: python
   :caption: ``typing.cast`` で型を明示する
   :force:

   def get_column_value(item: Tag, propname: str) -> str:
       if prop := item.find(string=propname):
           column = prop.find_next("td")
           if isinstance(column, Tag):
               return cast(str, column.text).strip()
       ...

コードを本質的に修正せずにエラーを黙らせる
----------------------------------------------------------------------

応急処置として |mypy| を黙らせる方法を記す。最終的にはコードのほうを正しく書くこ
とで沈黙させろ。

* インラインコメント :samp:`# type: ignore[{NAME}]` をエラー行の末尾に挿れる。
* コマンドラインオプション :samp:`--disable-error-code NAME` を付けて実行する。

代用ファイル
----------------------------------------------------------------------

型注釈の与え方として、これまで記してきたのは既存の Python ファイルに型を直接書き
込む方式だった。これをインライン方式と呼ぶ。もう一つの与え方に、拡張子 .pyi の代
用ファイルを設けるものがある。おそらく、特に、ライブラリーの機能が Python 以外の
言語で実装されているなど、インライン型注釈が物理的に不可能である場合の代替法だと
考えられる。

拡張子が .pyi のファイル
   対応する名前のモジュールが含む型付きオブジェクトの型注釈を記したファイル。
ファイル :file:`py.typed`
   代用システムを採用しているという目印。

オーバーロード
----------------------------------------------------------------------

   If a function or method can return multiple different types and those types
   can be determined based on the presence or types of certain parameters, use
   the ``@overload`` mechanism defined in `PEP 484`_. When overloads are used
   within a ".py" file, they must appear prior to the function implementation,
   which should not have an ``@overload`` decorator. (`Typing Python Libraries`,
   <https://typing.readthedocs.io/en/latest/guides/libraries.html>)

リンク先を見ると組み込み型の機能における実装例を示している。これは後回しでいいか。

統合
======================================================================

Visual Studio Code
----------------------------------------------------------------------

Visual Studio Code 拡張に mypy_ を支援するものがある。詳細は VS Code のサイドバー
:guilabel:`EXTENSIONS` パネルの検索結果欄からそれぞれのヘルプページを見ろ。

Mypy
   Matan Gover 氏による拡張パック。使用者環境の |mypy| を用いるもよう。
Mypy Type Checker
   Microsoft による拡張パック。これ自体に |mypy| が付属されているもよう。Python
   拡張が別途必要。

どちらでも良さそうなので、前者の拡張をインストールしておく。インストールが完了し
たら :kbd:`Ctrl` + :kbd:`,` で構成ファイルを開いて編集する。GUI を使う場合には検
索欄に ``mypy`` と入力して項目を絞り込め。ユーザー用とプロジェクト用の区別に気を
つけろ。

.. sourcecode:: json
   :caption: :file:`settings.json` 構成例
   :force:

   {
     "mypy.configFile": "/path/to/mypy.ini",
     "mypy.runUsingActiveInterpreter": true
   }

.. seealso::

   :doc:`/vscode/extensions`

資料集
======================================================================

`mypy documentation`_
   公式文書。First Step 章にあるページが重要だ。
`mypy - Optional Static Typing for Python <https://mypy-lang.org/index.html>`__
   公式ブログ。About から開発陣の簡単な紹介を読むことが可能。Examples にあるコー
   ドにおける型注釈は現在の Python 仕様を用いれば、コメントでない形式で書ける。
`PEP 484 - Type Hints`_
   Python 型ヒント仕様と考えられる。
`Static Typing with Python <https://typing.readthedocs.io/en/latest/>`__
   Type System Reference を通読して型理論の中核概念を理解しろ。かなりの数の例
   コードで |mypy| がエラーを出すのがかなり気になるが。
`Pros and Cons of Type Hints <https://realpython.com/lessons/pros-and-cons-type-hints/>`__
   型ヒント機能にまつわる長所と短所の比較論考。Real Python 内記事。
`Static type checking <https://learn.scientific-python.org/development/guides/mypy/>`__
   Python コード静的型チェックの何たるかを議論。Scientific Python Development
   Guide 内記事。
`The Comprehensive Guide to mypy <https://tusharsadhwani.medium.com/the-comprehensive-guide-to-mypy-b7cd502d04e3>`__
   すばらしい記事。Python 側の仕様進化により、用いる型やモジュールが若干古いのに
   は注意する。
`Mypy is a waste of time · Issue #11492 · python/mypy <https://github.com/python/mypy/issues/11492>`__
   静的型解析アンチに対する反論に学びたい。

.. include:: /_include/python-refs-core.txt
.. _mypy:
.. _mypy documentation: https://mypy.readthedocs.io/en/stable/
.. _PEP 484:
.. _PEP 484 - Type Hints: https://peps.python.org/pep-0484/
.. _Ruff: https://docs.astral.sh/ruff/
