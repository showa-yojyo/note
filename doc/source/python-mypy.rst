======================================================================
mypy 利用ノート
======================================================================

.. |conda| replace:: :program:`conda`
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

.. todo::

   関連ツール

   * VS Code Pylance extension

   Python コード

   * 当分は ``from __future__ import annotations`` を入れておくのが無難
   * ``from typing import TYPE_CHECKING`` などの定型文メモ
   * ``reveal_type(X)`` の正しい使い方
   * ``Union[X, None]``, ``Optional[X, None]``, ``X | None``
   * ``Any`` をなるべく書かない
   * ``TypedDict``, ``NamedTuple``
   * ``NoReturn``, ``Never``
   * ``Self``
   * ``Callable``
   * あのグラフを用意したい
   * ``@overload`` は使ったことがない
   * ``.pyi`` ファイル
   * :file:`py.typed` ファイル

資料集
======================================================================

`mypy documentation`_
   公式文書。First Step 章にあるページが重要だ。
`mypy - Optional Static Typing for Python <https://mypy-lang.org/index.html>`__
   公式ブログ。About から開発陣の簡単な紹介を読むことが可能。Examples にあるコー
   ドにおける型注釈は現在の Python 仕様を用いれば、コメントでない形式で書ける。
`PEP 484 - Type Hints`_
   Python 型ヒント仕様と考えられる。
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
