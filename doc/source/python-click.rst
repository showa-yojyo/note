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

画面への出力には関数 ``click.echo`` を使え
----------------------------------------------------------------------

公式文書によれば、関数 ``click.echo`` を Python 標準 ``print()`` の代わりとして
なるべく使えとある。さまざまなデータ、ファイル、環境に対してより良く働く。

個人的に好きな性質を挙げる：

* 色や単純な書式付きでテキストを出力可能。例えば赤い太字とか。
* 出力が対話型端末でなさそうな場合、ANSI 色とスタイルコードを削る。
* 出力をつねにフラッシュする。

.. todo::

   Python 標準 ``logging`` との棲み分けは？

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

* 当然ながら ``helloworld.py`` のみ。
* ``helloworld.py --help``: オプション ``--help`` も自動的に組み込まれる。

このオプションを付けてスクリプトを走らせると、ヘルプを表示して終了する。そのとき
の本文はコマンド関数の docstring から構成される。Click_ はこのテキストを端末画面
の幅に合わせて折り返し表示する。エディターに入力したとおりに画面に出力させるには
制御文字 ``\b`` を用いる。解除は ``\f`` だ。

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

   __version__ = "1.0.0"

   @command()
   @click.version_option(__version__, help="show the version and exit")
   def main(): ...

   if __name__ == "__main__":
       main()

このスクリプトの名前を :file:`myapp.py` とすると、これだけでコマンドライン
``myapp.py --version`` が有効となる。

フラグ名を ``--version`` だけではなく ``-V`` にも対応するには、バージョン実引数
のすぐ次からキーワード実引数すべての直前までにフラグ名を列挙すればいい：

.. sourcecode:: python
   :caption: "-V" と "--version" の両方をバージョンフラグとする
   :force:

   @command()
   @click.version_option(__version__, "-V", "--version")
   def main(): ...


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

.. _click-anchor-path:

コマンドライン引数をファイルパスとする
----------------------------------------------------------------------

ファイルパスを引数にとるスクリプトを作成する機会は頻繁にある。コマンドライン引数
として複数のパス文字列を取るコマンドを作る場合には、次のようにするのがよい。

.. sourcecode:: python
   :caption: ``type=click.Path`` の適用例
   :force:

   import pathlib
   import click

   @click.command()
   @click.argument(
       "file",
       nargs=-1,
       type=click.Path(
           exists=True,
           path_type=pathlib.Path,
       ),
   )
   def main(file): ...

Python コードではコマンド関数 ``main`` の最初の仮引数名が ``@click.argument`` の
最初の実引数値と同じになる。

* ``myapp.py file1 file2`` のようなコマンドが許される。
* ``nargs=-1`` のおかげでパスを全く指定しないコマンドも許される。この手のイン
  ターフェイスはそう設計するのが鉄則だ。
* 急所は ``type=click.Path(...)`` だ。これは引数 ``file`` がファイルシステムの有
  効なパス文字列であることを保証する。コンストラクターに渡す値により、そのパス文
  字列の条件を柔軟に指定することが可能だ。例えば、

  * ``exists=True`` により、存在するファイルパスしか指定を許さない。
  * ``path_type=pathlib.Path`` により、関数 ``main`` の引数としての ``file`` の
    型を ``pathlib.Path`` に変換させる。後続のパス操作に便利であるがゆえ、このパ
    ス型指定を与えたい。

``@click.option`` 系デコレーターでよく使うキーワード引数
----------------------------------------------------------------------

``@click.option`` 系デコレーターでよく使うキーワード引数はクラス ``Option`` のコ
ンストラクターが取る引数とだいたい一致する。よく使用するものを下に載せる：

``help``
   ヘルプ文字列。自作オプションに対しては必ず指定しろ。
``type``
   オプション値の型。これを適切に指定しておくと、Click_ がコマンドラインからの入
   力値を検証してから、値を所望の型に変換するか、エラーで終了する。Python 組み込
   み型を渡す場合もあるが、パスや日付など、土台は文字列だが特別な書式をとる値に
   対して機能する専用型も Click_ は備えている。後ほど個別に記すが、例を挙げる：

   * ``click.Choice``
   * ``click.DateTime``
   * ``click.File``
   * ``click.Path``

``is_flag``
   オプションをフラグとして機能させたい場合には値を ``True`` に明示的に指示しろ。
   指定しない場合には Click_ がオプション型を自動的に判断する。
``show_default``
   コマンドヘルプ表示において、当該オプションの既定値をヘルプ画面に出すかどうか
   を指定する。Click_ は ``False`` を既定とするが、一律 ``True`` でいいと思う。
``show_envvar``
   当該オプションが環境変数に対応している場合、コマンドヘルプ表示にその変数名を
   示すかどうかを指定する。一律 ``True`` でいいと思う。

構成ファイル実装
----------------------------------------------------------------------

Git でいうところのファイル :file:`.gitconfig` のような機能を実現する手順を記す。

まず、コマンドラインオプション ``-c FILE`` または ``--config FILE`` で構成ファイ
ルを指定するインターフェイスを定義する：

.. sourcecode:: python
   :caption: オプション ``--config`` 搭載例
   :force:

   import pathlib
   import click

   @click.command()
   @click.option(
       "-c",
       "--config",
       type=click.Path(exists=True, path_type=pathlib.Path),
       default=None,
       metavar="PATH",
       callback=configure,
       is_eager=True,
       expose_value=False,
       help="path to config file",
   )
   def main(): ...

キーワード引数を指定する狙いは次のとおり：

* ``type=click.Path(...)`` の行の目的は先述のとおり、既存のファイルパスを与えら
  れることを保証したい。
* ``is_eager=True`` であるオプション値は、そうでない値のものより先に処理される。
  構成ファイル処理を急いているのだ。これを利用して構成ファイルを先に読み込むのが
  目的だ。
* ``expose_value=False`` を指定して、関数 ``main`` の引数リストに対応する引数を
  与えなくて済むようにする。構成ファイル処理を ``main`` で行うわけではないのだ。
* ``callback=configure`` を指定して、構成ファイルを読み込む関数を呼び出すように
  指示する。ここでは関数 ``configure`` を呼び出させる。

別途コールバック関数 ``configure`` を実装する。次の例のコードは構成ファイルの書
式を YAML であるとしている。

.. sourcecode:: python
   :caption: 構成ファイル読み込み例
   :force:

   import yaml

   def configure(ctx, param, value):
       if value:
           assert isinstance(value, pathlib.Path)
           with open(value, mode="r") as fin:
               ctx.default_map = yaml.safe_load(fin)
       return value

辞書 ``ctx.default_map`` とはコマンドラインオプションの既定値を含むデータであり、
YAML ファイル内容の値を使ってそれを初期化するという理解でいい。

関数 ``click.get_app_dir``
----------------------------------------------------------------------

構成ファイル読み込み処理にも関連するのだが、その既定パスを決定するのに関数
``get_app_dir`` が有用だ。アプリケーションやパッケージの名前を指定すると、その構
成ディレクトリーパス文字列を得られる。

既定動作では OS に最適のパスを返す。例えば WSL を含む Linux では：

.. sourcecode:: pycon
   :caption: ``click.get_app_dir`` 使用例
   :force:

   >>> import click
   >>> APP_NAME = "myapp"
   >>> click.get_app_dir(APP_NAME)
   '/home/username/.config/myapp'
   >>> click.get_app_dir(APP_NAME, force_posix=True)
   '/home/username/.myapp'

これを先述した構成ファイル読み込みコードに組み込むのが良い。オプション ``-c``,
``--config`` が与えられていない場合には、既定の構成ファイルパスとしてこの値を用
いるとらしくなる。

気の利いた引数型
----------------------------------------------------------------------

デコレーター ``@click.option`` キーワード引数 ``type`` に指定可能である専用型の
うち、特に便利なものをいくつか記す。

入力値の集合がある場合には ``click.Choice`` を使え
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用例を次に示す。キーワード引数 ``case_sensitive`` の既定値が ``True`` であるの
が不便であると考えられる場合には ``False`` に変えろ：

.. sourcecode:: python
   :caption: ``click.Choice`` 使用例
   :force:

   @click.command()
   @click.option(
       "-f",
       "--format",
       type=click.Choice(
           ("json", "jsonline", "xml", "csv"),
           case_sensitive=False,
       ),
       default="json",
   )
   def main(format): ...

日付または時刻に ``click.DateTime`` を使え
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

時刻まで欲しい場合には ``click.DateTime`` コンストラクターを引数指定なしで呼び出
せば十分だ。

時刻不要の日付を扱う場合はコード側での対応が生じる場合がある。次のように指定する
場合でも ``click.DateTime`` オブジェクトは時刻情報を有する：

.. sourcecode:: python
   :caption: ``click.DateTime`` 使用例
   :force:

   @click.command()
   @click.option(
       "--since",
       type=click.DateTime(("%Y-%m-%d",)),
       metavar="DATE",
   )
   def main(since): ...

日付部分だけを得るには、呼び出し側で `` 00:00:00`` 部分をトリムしかない。

ファイル内容には ``click.File`` を使え
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

公式リポジトリーにある次のファイルが使用例だ：

   `click/examples/inout/inout.py <https://github.com/pallets/click/blob/main/examples/inout/inout.py>`__

Python コード中で標準入力と普通のファイルを区別せずに扱うのがこの型の目的だ。関
連して、関数 ``click.open_file`` は同様の思想で設計されている。

ファイルパスには ``click.Path`` を使え
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

先述した :ref:`click-anchor-path` のとおり。

実行中に入力を受け付けてもよい場合は ``prompt=True`` を使え
----------------------------------------------------------------------

スクリプト実行中に端末からのキーボード入力による値を受け付けたい。この場合には
キーワード引数 ``prompt=True`` を指定しろ。使用例：

.. sourcecode:: python
   :caption: ``prompt=True`` 使用例
   :force:

   @click.command()
   @click.option(
       "-u",
       "--user",
       prompt=True,
       hide_input=False,
       metavar="NAME",
   )
   def main(user): ...

コマンドラインから ``-u`` または ``--user`` をその実引数と共に指定して実行すると
プロンプトが出ることなくプログラムが進行する。どちらも指定せずに実行すると
``User:`` のプロンプトで標準入力が開き、キーボード入力を待機する。

パスワード入力には ``@click.password_option`` を使え
----------------------------------------------------------------------

上述の要領でパスワードオプションを定義しても良いが、ありがちなオプションであるの
で Click_ がすでに用意している：

.. sourcecode:: python
   :caption: ``@click.password_option`` 使用例
   :force:

   import click

   @click.command()
   @click.password_option(metavar="PASSWORD")
   def main(password): ...

この例ではコマンドラインオプションは ``--password`` となり、コマンド関数の引数名
は ``password`` となる。コマンドラインでパスワードを指定することが可能であるう
え、未指定実行時にはプロンプト入力方式になる。

キーボード入力時にタイプしたキーは端末にエコーされない。

プロンプトは確認用と合わせて二度出現する。

その他
----------------------------------------------------------------------

* ``@click.pass_context`` について述べたい。
* 構成ファイルに関連して環境変数からオプション値を読み込む方法を扱いたい。

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
   を ``click.echo()`` などに置き換えたり、``None`` を ``0.0`` に変えるなど、改
   良点や修正点を探しつつ読め。

   標準の ``argparse`` にあって Click_ にはない機能を挙げている記事は初めて見た。
`Advanced CLI structures with Python and Click <https://mauricebrg.com/article/2020/08/advanced_cli_structures_with_python_and_click.html>`__
   少し発展的な機能を紹介する記事。コマンド集約や独自入力検証など。ブログ内には
   Click_ 関連記事が他にもある。
`command line interface - Python Click - Supply arguments and options from a configuration file <https://stackoverflow.com/questions/46358797/python-click-supply-arguments-and-options-from-a-configuration-file>`__
   構成ファイルの実装方法が複数示されている。

.. todo::

   バージョン実装の参考になった資料があったのだが、URL を忘れた。あらためて
   Google 検索を試したが、記憶にあるものと一致するものが見つからなかった。

.. include:: /_include/python-refs-core.txt
.. _Click:
.. _Click Documentation: https://click.palletsprojects.com/en/stable/
