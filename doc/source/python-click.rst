======================================================================
Click 利用ノート
======================================================================

.. |conda| replace:: :program:`conda`
.. |CLI| replace:: :abbr:`CLI (Command Line Interface)`
.. |pyproject| replace:: :file:`pyproject.toml`

.. contents:: 章見出し
   :local:

概要
======================================================================

Python で |CLI| を書くときに Click_ はたいへん便利なパッケージだ。次のような機能
を搭載している：

* Unix/POSIX コマンドライン規約の実装
* 環境変数からの値の読み込み
* カスタム値のプロンプト
* 入れ子コマンド
* ファイル処理
* 便利補助機能各種

  * 端末寸法取得
  * ANSI 色使用
  * キーボード直接入力取得
  * 画面消去
  * 構成ファイルパス検索
  * テキストエディターなどの起動

インストール・更新・アンインストール
======================================================================

複数人で共用するプロジェクトの開発環境に Click_ をインストールする事例では、その
プロジェクトの定める手順に従え。README や |pyproject| を読めば判明する。

自分が所有する作業用仮想環境にインストールするならば、愛用している仮想環境ツール
がインストールコマンドを実装している場合にはそれを使え。私ならば Miniconda_ であ
るから、例えば次のようにする：

.. sourcecode:: console
   :caption: 現在の conda 仮想環境に Click をインストールする
   :force:

   $ conda install -c conda-forge click

インストール手順の説明は以上だ。Click_ の更新、アンインストールの手順は、対応す
る条件におけるインストール手順に合致する手順を選べ。例えば |conda| を使っている
のならば ``conda uninstall click`` を走らせる。

.. seealso::

   :doc:`/python-miniconda`
      |conda| を使ってインストールする場合、更新やバージョン確認にもそれを用い
      る。

使用方法・コツ
======================================================================

単一コマンドしかないような単純なスクリプトを作成する場合ですらよく使う手筋を記
す。

Python 関数をコマンドに仕立てる
----------------------------------------------------------------------

Click_ を用いるもっとも単純なスクリプトは次のようなコードだ：

.. sourcecode:: python
   :caption: ``import click`` を含む最小スクリプト
   :force:

   import click

   @click.command()
   def main():
       """Output a text."""
       click.echo("Hello world.")

   if __name__ == "__main__":
       main()

このスクリプトの名前を :file:`helloworld.py` とすると、これだけで次のコマンドラ
インが有効だ：

* ``helloworld.py``
* ``helloworld.py --help``: オプション ``--help`` も自動的に組み込まれる。

オプション ``--help`` を調整する
----------------------------------------------------------------------

既存のオプション説明文と整合させるために ``@click.help_option`` などを明示的に用
いて ``--help`` 自身のヘルプ文言を独自化することが可能だ。

.. sourcecode:: python
   :caption: ``@click.help_option`` を使って説明文を自分で決める
   :force:

   import click

   @command()
   @click.help_option(help="show this message and exit")
   def main(): ...

   if __name__ == "__main__":
       main()

オプション ``--version`` を実装する
----------------------------------------------------------------------

Click_ が用意している ``@click.version_option`` を再利用するのが手っ取り早い。コ
マンド定義関数からアプリケーションまたはパッケージのバージョン文字列が参照可能で
ある場合には次のようにするのが自然だ：

.. sourcecode:: python
   :caption: ``@click.version_option`` を使って ``--version`` を実装する
   :force:

   import click

   @command()
   @click.version_option(__version__, help="show the version and exit")
   def main(): ...

   if __name__ == "__main__":
       main()

このスクリプトの名前を :file:`myapp.py` とすると、これだけでコマンドライン
``myapp.py --version`` が有効となる。

より詳細なバージョン出力を備えたい場合には ``version_option`` ではなく、汎用の
``option`` を用いる。さらにコールバックで実装する：

.. sourcecode:: python
   :caption: ``@click.option`` を使って ``--version`` を自前で実装する
   :force:

   import sys
   import click

   def print_version(
       ctx: click.Context,
       param: click.Parameter,
       value: bool,
   ) -> None:
       """Display version information and exit."""

       if not value or ctx.resilient_parsing:
           return

       click.echo(f"myapp.py: {__version__}")
       click.echo(f"Click: {click.__version__}")
       click.echo(f"Python: {sys.version}")
       ctx.exit()


   @click.command()
   @click.option(
       "-V",
       "--version",
       is_flag=True,
       callback=print_version,
       expose_value=False,
       is_eager=True,
       help="display version information and exit",
   )
   def main(): ...

.. todo::

   参考にした Stack Overflow のスレを引用する。


.. * docstring での改行
.. * ``@click.command``
.. * ``@click.argument``
.. * ``@click.option`` でよく使うキーワード引数
..
..   * ``metavar``
..
..      * `metavar` に使えない文字がある？
..   * ``type``
..   * ``default``
..   * ``is_flag``
.. * ``click.echo``
.. * ``click.get_app_dir``
.. *
.. * 構成ファイル実装
..
..   * ``@click.pass_context``
.. * ユーザー名とパスワード ``@click.password_option``
.. * ``type=click.Path`` で ``path_type`` を指定する
.. * ``type=click.Choice``
.. * 日付型オプション (`type=click.DateTime(...)`)

.. todo::

   Click_ を愉しみながら執筆する。リンク追加。

資料集
======================================================================

`Click Documentation`_
   公式文書。
`Click and Python: Build Extensible and Composable CLI Apps <https://realpython.com/python-click/>`__
   チュートリアル。Real Python の記事。Click_ を用いたプログラムを配布するための
   プロジェクト構成ファイル |pyproject| の書き方を示しているのはありがたい。
`Working with Python Click Package <https://chuan-zhang.medium.com/working-with-python-click-package-51602dc0ba2f>`__
   紹介とささやかなチュートリアルからなる記事。Python パッケージを説明する前に、
   開発の全ては仮想環境で行うと断れば、残りの記述が簡潔になりがちになることを
   習った。
`Python click or how to write professional CLI applications <https://www.mndwrk.com/blog/python-click-or-how-to-write-professional-cli-applications>`__
   詳しめの紹介記事。自作 JSON 解析スクリプトのリファクタリングを通じて上手く説
   明している。このコードをそのまま受け入れて読むのではなく、例えば ``print()``
   を``click.echo()`` などに置き換えたり、``None`` を ``0.0`` に変えるなど、改良
   点や修正点を探しつつ読め。

   標準の``argparse`` にあって Click_ にはない機能を挙げている記事は初めて見た。
`Advanced CLI structures with Python and Click <https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html>`__
   少し発展的な機能を紹介する記事。コマンド集約や独自入力検証など。ブログ内には
   Click_ 関連記事が他にもある。

.. include:: /_include/python-refs-core.txt
.. _Click:
.. _Click Documentation: https://click.palletsprojects.com/en/stable/
