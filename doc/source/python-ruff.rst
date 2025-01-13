======================================================================
Ruff 利用ノート
======================================================================

.. contents:: 章見出し
   :local:

概要
======================================================================

公式文書冒頭によると、Ruff_ は自らを次のように規定している：

   An extremely fast Python linter and code formatter, written in Rust.

静的解析や書式整形を超高速に実行するのはありがたい。Ruff_ はさらに、先行する同種
の道具の上を行くと豪語している：

   Ruff can be used to replace Flake8 (plus dozens of plugins), Black, isort,
   pydocstyle, pyupgrade, autoflake, and more, all while executing tens or
   hundreds of times faster than any individual tool.

Ruff_ が比較対象に挙げているものを現在利用しているのであれば、乗り換えを検討する
価値がある。

.. seealso::

   :doc:`/python-pylint`

インストール・更新・アンインストール
======================================================================

複数人で共用するプロジェクトの開発環境に Ruff_ をインストールする事例では、その
プロジェクトの定める手順に従え。README や :file:`pyproject.toml` を読めば判明す
る。

自分が所有する作業用仮想環境にインストールするならば、愛用している仮想環境ツール
がインストールコマンドを実装している場合にはそれを使え。私ならば Miniconda_ であ
るから、例えば次のようにする：

.. sourcecode:: console
   :caption: 現在の conda 仮想環境に Ruff をインストールする
   :force:

   conda install -c conda-forge ruff

インストール手順の説明は以上だ。Ruff_ の更新、アンインストールの手順は、対応する
条件におけるインストール手順に合致する手順を選べ。例えば :program:`conda` を使っ
ているのならば ``conda uninstall ruff`` を走らせる。

.. seealso::

   :doc:`/python-miniconda`

構成・カスタマイズ
======================================================================

構成ファイルパス
----------------------------------------------------------------------

   Ruff looks for the first :file:`pyproject.toml`, :file:`ruff.toml`, or
   :file:`.ruff.toml` file in the file's directory or any parent directory.

記述の都合上、本稿では構成ファイルとして後者を用いる。これは基本的には対象プロ
ジェクトのルートディレクトリーにだけ置くのがわかりやすい。ディレクトリー階層的に
最も近い位置にあるものを :program:`ruff` は採用するが、そのような構成ファイルが
見当たらない場合、使用者固有の構成ファイルを探しに行く。Linux では次のパスが候補
となる：

:file:`$XDG_CONFIG_HOME/ruff/ruff.toml`

.. seealso::

   * <https://docs.astral.sh/ruff/faq/#how-can-i-change-ruffs-default-configuration>
   * <https://docs.rs/etcetera/latest/etcetera/#native-strategy>
   * :doc:`/xdg`

構成方式
----------------------------------------------------------------------

Ruff_ の機能は Python コードに対する静的解析と書式整形だ。コマンド ``ruff
check`` が静的解析を、``ruff format`` が書式整形をそれぞれ行う。構成ファイルの区
画 ``[lint]`` と区画 ``[format]`` それぞれで機能の挙動を調整可能だ。

区画 ``[lint]`` では ``select``, ``ignore`` などに対象規則を指定する。

.. sourcecode:: toml
   :caption: :file:`ruff.toml` コード解析オプション指定例
   :force:

   [lint]
   select = ["I",]
   ignore = ["PLC0415",]

* 原子規則は英文字プラス三桁の数字で構成される。E.g. ``D203``, ``F401``.
* 英文字だけを指定することが可能だ。その文字から始まる原子規則すべてを指定する
  ことになる。
* 使わないが、特殊規則 ``ALL`` はすべての規則を意味する。競合規則は Ruff_ が適宜
  調停する。

区画 ``[format]`` では書式整形オプションを指定する。二つある引用符をどちらに統一
したいのかを明記することなどにも役に立つ。

.. sourcecode:: toml
   :caption: :file:`ruff.toml` 書式整形オプション指定例
   :force:

   [format]
   # Enable reformatting of code snippets in docstrings.
   docstring-code-format = true
   docstring-code-line-length = "dynamic"

   # Use 4 space indentation.
   indent-style = "space"

   # Use `\n` line endings for all files.
   line-ending = "lf"

   # Enable preview style formatting.
   preview = true

   # Prefer single quotes over double quotes.
   quote-style = "single"

   # Ignore the magic trailing comma.
   skip-magic-trailing-comma = true

.. seealso::

   * <https://docs.astral.sh/ruff/settings/#format>

グローバルスコープにはそれ以外の項目を指定する。特にキャッシュ置場を設定しておく
のがおすすめだ。ファイルの先頭に配置するのがよい。

.. sourcecode:: toml
   :caption: :file:`ruff.toml` グローバル部分例
   :force:

   # Use $XDG_CACHE_HOME/ruff
   cache-dir = "~/.cache/ruff"

   # Allow lines to be as long as 88.
   #line-length = 88

   # PEP 8 recommends using 4 spaces per indentation level.
   indent-width = 4

   target-version = "py313"

使用方法・コツ
======================================================================

プロジェクトの仮想環境管理ツールに Ruff を組み込むコマンド
----------------------------------------------------------------------

Ruff_ 公式文書ではコマンド ``uv init --lib numbers`` を実行してからコマンド ``uv
add --dev ruff`` を実行することで依存関係を追加的に定義する手順を紹介している。
実際には、プロジェクトファイル :file:`pyproject.toml` に次の構成が追加される：

.. sourcecode:: toml
   :caption: :file:`pyproject.toml` の部分的な例
   :force:

   [dependency-groups]
   dev = [
       "ruff>=0.9.1",
   ]

開発者は仮想環境管理ツールのインストールコマンドを実行して、依存関係として Ruff_
をインストールする。または、ツールによっては ``run`` や ``shell`` のようなコマン
ドがあり、それらの実行時に Ruff_ を自動的にインストールする。

Ruff_ コマンドを実行するときも、仮想環境管理ツールの上記のようなコマンドを経由す
る。

静的解析コマンド
----------------------------------------------------------------------

コマンド ``ruff check`` で Python コードのマズい箇所を解析、報告させる。使えそう
なコマンドラインパターンを記す。

引数なしで Ruff_ コマンドを実行する場合はプロジェクトにある Python コード全体が
解析対象となる。引数にディレクトリーを指定すると、そことそこから下にあるコードす
べてが解析対象となる。引数にファイルを直接指定すると、それのみが解析対象となる。


``ruff check --show-settings``
   コード解析構成を TOML 書式で出力する。例えば ``linter.rules.enabled`` の値を
   見ると解析対象規則がわかる。
``ruff check``
   マズい箇所を含むファイルパス、行数、規則番号を報告する。
``ruff check --fix``
   上記コマンドの報告動作に加え、マズい箇所が機械的かつ安全に修正可能である場合
   にそれを修正する。
``ruff check --statistics``
   規則違反の総数を表示する。これは便利だ。

   .. sourcecode:: console
      :caption: ``ruff check --statistics`` 実行例
      :force:

      $ ruff check --statistics
      292     F405    [ ] undefined-local-with-import-star-usage
       50     F403    [ ] undefined-local-with-import-star
       26     E741    [ ] ambiguous-variable-name
       17     E402    [ ] module-import-not-at-top-of-file
        4     E721    [ ] type-comparison
        1     E731    [*] lambda-assignment
      [*] fixable with `ruff check --fix`

``ruff check --unsafe-fixes``
   その機械的修正が安全でないものも報告させる。
``ruff check --fix --unsafe-fixes``
   上記コマンドの報告動作に加え、安全性を問わず修正対象であるものをすべて修正さ
   せる。
``ruff check --watch``
   プロジェクトのファイルすべてを解析し、変更が生じるタイミングで再解析させる。
   サーバーが走るので、バックグラウンド実行が良い。
``ruff check --extend-select RUF100``
   コードが含む意味のない ``noqa`` 指令を拾う。対象ファイルを変更しない。
``ruff check --extend-select RUF100 --fix``
   上記コマンドによる報告に加え、そのような指令に違反するコードをファイルから除
   去する。
``ruff check --select --add-noqa``
   対象ファイルについて、違反を含む行のすべてに ``noqa`` 指令を追加させる。
   Python プロジェクトに Ruff_ を導入する段階の初動で実行するのが望ましい。

どの規則を自動修正可能であるとみなすかを、コマンドラインまたは構成ファイルから指
定することが可能だ。

書式整形コマンド
----------------------------------------------------------------------

コマンド ``ruff format`` で Python コードの書式を整形する。使えそうなコマンドラ
インパターンを記す。

``ruff format``
   書式整形を行わせる。引数に関する注意は静的解析コマンドと同じ。以下同様。
``ruff format --check``
   書式整形対象であるファイルを一覧表示させる。対象ファイルを変更させない。
``ruff format --diff``
   書式整形対象であるファイルそれぞれに対して、その内容を変更することなく整形前
   後の差分を表示させる。端末で作業をしているときに多用したいコマンドだ。

Ruff に特別な処理をさせるコメント集
----------------------------------------------------------------------

Python コードにコメントとして特定のパターンを記載しておくと、Ruff_ の挙動が対応
するコマンドラインオプション・構成ファイル内容の指示どおりになる。そのようなコメ
ント書式をいくつか挙げる。

Flake8 方式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

行末コメント :samp:`# noqa: {code}`
   この行が含む規則番号 `code` の違反を Ruff_ に見逃すように指示する。公式文書で
   はこれを Flake8 方式と呼んでいる。

   規則を複数指定する場合は番号をカンマで区切って並べればいい。

   .. sourcecode:: python
      :caption: アクションコメント例
      :force:

      some_code  # noqa: E741, F841

行末コメント ``# noqa``
   この行が含む規則違反すべてを Ruff_ に見逃させる。こんな粗い指示をしてはいけな
   い。
インポート文塊の最初の行に置く行末コメント ``# noqa: I001``
   インポート文塊に対する整列修正に対する Ruff_ への抑制指示。
コメント :samp:`# ruff: noqa: {code}`
   ファイル全体にわたって規則 `code` に対する違反をすべて無視する。通常、このコ
   メントだけを記した行をファイルの先頭に挿れる。
コメント ``# ruff: noqa``
   ファイル全体にわたって違反すべてを無視する。こちらもファイルの先頭に挿れるの
   が普通だ。

isort 方式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

次のコメント指令はコードブロックやその他のインライン構成に対して、インポートの並
べ替えを選択的に有効または無効にするように指示するものだ。

インポート文の行末コメント ``# isort: skip``, ``# ruff: isort: skip``
   当該 ``import`` 文を整列対象にさせない。この行を一般コードとして扱わせ、ファ
   イル内 ``import`` 文区画下に押し下げる。
インポート文塊前にあるコメント行 ``# isort: skip_file``, ``# ruff: isort: skip_file``
   ファイル全体にわたってインポート整列を省略させる。
インポート文塊前にあるコメント行 ``# isort: off``, ``# ruff: isort: off``
   次の行以降、整列解析を切る。
インポート文塊前にあるコメント行 ``# isort: on``, ``# ruff: isort: on``
   整列解析が切れていた場合、それを復活させる。
インポート文塊間にあるコメント行 ``# isort: split``, ``# ruff: isort: split``
   このコメント行の直前までの整列をいったん確定し、直後のインポート文塊を別の塊
   として途整列させる。

書式整形抑制指令
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コマンド ``ruff format`` が対象とする整形範囲をコード中からコメントで指示するこ
とが可能だ。

コメント ``# fmt: off`` および ``# fmt: on``
   整形範囲境界を文単位で指示する。
コメント ``# yapf: disable`` および ``# yapf: enable``
   上とまったく同様。
コメント ``# fmt: skip``
   直前にある文、デコレーター、関数定義、クラス定義の整形を抑制する。

pre-commit フック
----------------------------------------------------------------------

Ruff_ は pre-commit_ フックを公開している。これにより規則違反のコードをリポジト
リーに commit してしまう事故を未然に防止できるだけでなく、生のコードを整形してリ
ポジトリーに更新することも可能だ。

プロジェクトにある YAML ファイル :file:`.pre-commit-config.yaml` に当該フックを
搭載する GitHub リポジトリー情報およびフック仕様を追記しろ：

.. sourcecode:: yaml
   :caption: :file:`.pre-commit-config.yaml` に Ruff フックを組み込む例
   :force:

   repos:
   - repo: https://github.com/astral-sh/ruff-pre-commit
     rev: v0.9.2
     hooks:
       - id: ruff
         args: [ --fix ]
       - id: ruff-format

インポート文の塊を整列する方法
----------------------------------------------------------------------

``ruff check --select I --fix``
   インポート文の塊を整列する。実行するのはコマンド ``ruff format`` の直前がよい。

.. admonition:: 利用者ノート

   構成ファイル ``[lint]`` 区画に対応番号を含めておけばいい？

VS Code 拡張
----------------------------------------------------------------------

Visual Studio Code サイドバー :guilabel:`EXTENSIONS` パネルの検索欄で Ruff と入
力すると現れる拡張をインストールし、機能を有効にするとコマンドパレットから関連コ
マンドを実行することが可能になる。

.. seealso::

   :doc:`/vscode/extensions`

次のような機能がある：

* 右クリックメニュー :menuselection:`Quick Fix...` から解析した規則違反を一覧表
  示する。
* コマンドパレットから :menuselection:`Ruff: Fix all auto-fixable problems` コマ
  ンドを選択して、CLI での ``ruff check --fix`` 相当を実行する。
* コマンドパレットから :menuselection:`Ruff: Format document` コマンドを選択して、
  CLI での ``ruff format`` 相当を実行する。

この拡張の機能を完全に引き出すべく、VS Code の :file:`settings.json` で関連項目
を構成しておく。なお、構成ファイルのパスは Ruff_ が自動的に検出するものが採用さ
れるとある。

.. sourcecode:: json
   :caption: :file:`settings.json` 例
   :force:

   {
     "[python]": {
       "editor.codeActionsOnSave": {
         "source.fixAll": "explicit",
         "source.organizeImports": "explicit"
       },
       "editor.defaultFormatter": "charliermarsh.ruff",
       "editor.formatOnSave": true
     },
     "ruff.configuration": "/path/to/ruff.toml"
     "ruff.format.args": ["--config=/path/to/ruff.toml"]
     "ruff.lint.args": ["--config=/path/to/ruff.toml"],
   }

Bash 用タブ補完
----------------------------------------------------------------------

Bash のスタータップファイル :file:`.bashrc` の適当な行に次を書け：

.. sourcecode:: bash
   :caption: :program:`ruff` コマンドラインタブ補完を使えるようにするコマンド例
   :force:

   # Enable Ruff completion
   [ -x "$(command -v ruff)" ] && eval "$(ruff generate-shell-completion bash)"

GitHub Actions
----------------------------------------------------------------------

自前で Ruff をインストールして ``ruff check`` を実行するワークフローでは出力書式
オプション ``--output-format github`` を指定しろ。

あるいは、GitHub に公開済みの ``astral-sh/ruff-action@v3`` を利用することも可能
だ。

.. sourcecode:: yaml
   :caption: ``astral-sh/ruff-action`` 使用例
   :force:

   - uses: astral-sh/ruff-action@v3
     with:
       src: ["./src"]

どの規則を採用するのが良いか
======================================================================

コマンド ``ruff rules --all`` を実行すれば :program:`ruff` が支援する規則すべて
を出力する。しかし端末画面では読みにくいので Web ブラウザーを使え：
<https://docs.astral.sh/ruff/rules/>

   By default, Ruff enables Flake8's F rules, along with a subset of the E
   rules, omitting any stylistic rules that overlap with the use of a formatter,
   like ruff format or Black.

とあるので、まずは F 規則と E 規則を全部流し読みしておく。コードスタイルに関する
ものは飛ばす感じで。PEP8 に関する N 規則も重要。PERF 規則は効率に関わる。

.. admonition:: 利用者ノート

   構成ファイルやコマンドラインで F 規則を明示的に ``select`` するのは筋が悪いと
   いうことだ。

   上述の default を確認したいならば、コマンド ``ruff check --show-settings`` を
   走らせて、出力から ``linter.rules.enabled`` および ``liner.rules.should_fix``
   を検査すればいい。

Pyflakes (F)
----------------------------------------------------------------------

* F402: ループ変数にインポートした何かと同じ名前を付けてはダメだ。
* F{403,405}: :samp:`from {module} import *` はダメだ。
* F707: ``except:`` ブロックは書くなら最後に書け。
* F901: ``raise NotImplemented`` ではなく ``raise NotImplementedError`` が普通は
  正しい。

pycodestyle (E, W)
----------------------------------------------------------------------

Error (E) と Warning (W) の二本立て。

* E111: インデントの大きさは設定値の倍数でなければダメ。
* E{201..252}: 括弧や句読点と空白文字の入れ方はこのとおりにしないと素人然とする。
* E305: 空行が二行ないとダメな場合がある。
* E501: 一行の桁数は PEP8 なら 79 桁だが、Ruff_ では既定 88 桁。
* E722: 生の ``except:`` を書いてはダメだ。
* W{291..293}: 見えにくい空白文字。

mccabe (C90)
----------------------------------------------------------------------

<https://en.wikipedia.org/wiki/Cyclomatic_complexity>

isort (I)
----------------------------------------------------------------------

規則は二つしかなく、インポート文が整列済みであるか、必要なインポートが欠けていな
いかを調べる。

pep8-naming (N)
----------------------------------------------------------------------

コーディング規約のうち、識別子の名前に関するものの集合であると考えられる。

簡単な覚え方としては、何らかの名前が should be uppercase である規則がないという
ことだ。

pydocstyle (D)
----------------------------------------------------------------------

* D{100..107}: 公開要素に docstring がないということは論外。
* D300: 三重引用符記号は double quotes でなければダメだ。
* D404: 主語が this であってはならない。いきなり動詞から始めろ。

pyupgrade (UP)
----------------------------------------------------------------------

Python 言語バージョンが上がるときに構文などの様式を刷新するために設けられた規則
集と考えられる。コードが古ぼけないようにするべく重視したい。

* UP004: ``class MyClass(object): ...`` はもう古い。
* UP010: Python のアップグレードにより不要になる ``from __future__`` がそのうち
  生じる。
* UP{013,014}: ``typing.TypedDict``, ``typing.NamedTuple`` は継承して使う。
* UP015: 関数 ``open`` 呼び出し時の実引数 ``mode="r"`` は冗長だそうだ。
* UP030: 文字列メソッド ``format`` の中括弧参照において位置番号は明示しない。
* UP032: そもそも f-string をなるべく使え。
* UP038: 複数型チェックのときには ``isinstance(x, type1 | type2)`` のように縦棒
  を使って指定する。
* UP040: ``typing.TypeAlias`` ではなくキーワード ``type`` が今や使える。
* UP045: ``typing.Optional`` はもはや使わない。

flake8-2020 (YTT)
----------------------------------------------------------------------

Flake8 系はプラグイン方式を採っていて、プラグインごとに定まった規則集合に対して
Ruff_ が接頭コードを独自に与えて規則をまとめているようだ。

最初の YTT グループは ``sys.version`` および ``sys.version_info`` にまつわる規則
集だ。Python 3.13 を使用している現時点ではこれらの規則は不要だろう。

flake8-annotations (ANN)
----------------------------------------------------------------------

* ANN001: 関数定義の引数リストの仮引数それぞれに対して型注釈を与えろ。
* ANN{002,003}: 同じく仮引数 ``*args``, ``**kwargs`` に対しても型注釈を与えろ。
* ANN{201,202,204..206}: 関数定義の戻り値に対して型注釈を与えろ。
* ANN401: ``typing.Any`` で茶を濁すな。

.. todo::

   当トピックに関連する mypy 利用ノートを準備中。

flake8-async (ASYNC)
----------------------------------------------------------------------

.. todo::

   TBD

flake8-bandit (S)
----------------------------------------------------------------------

コードが何らかの危険や脅威から免れていることを保証するための規則集。Python に関
係のある規則もあるし、例えばパスワードをハードコードしてはならぬなど、言語の枠組
を超えた一般論として設けられた規則もある。

* S101: C/C++ 感覚で ``assert`` を使ってはいけない。まともな例外送出コードに書き
  換えろ。
* S102: 組み込み関数 ``exec`` を使うのはダメだ。
* S108: 一時ファイルを使うにはモジュール ``tempfile`` を使え。
* S{110,112}: ``except`` 節で何もしないのはダメで、ログファイルに何か書け。
* S113: ``timeout`` 引数があれば必ず指定しろ。
* S201: ``debug`` 引数をハードコードするのはダメだ。
* S301: 関数 ``pickle.load`` は直接的か間接的を問わず、使うのはダメだ。
* S303: SHA-256 はとりあえず使っていい。
* この辺の番号は専門的な内容が続くので割愛。
* S506: ``yaml.load`` ではなく ``yaml.safe_load``
* S{603,604}: ``shell=True`` は要注意。安全ではない。
* S607: 実行形式へのパスは絶対パスで指定しなければ安全でない。
* S608: SQL 文をハードコードするのはダメだ。
* S609: ``subprocess.Popen()`` の引数にワイルドカードを与えるのはダメだ。
* S701: Jinja2 使用時に引数 ``autoescape=True`` を与えろ。これは既定値ではない。

flake8-blind-except (BLE)
----------------------------------------------------------------------

次の例外処理節を使うのはダメだという規則。類似規則が他の節にもある。

* 裸の ``except``
* ``except BaseException``
* ``except Exception``

flake8-boolean-trap (FBT)
----------------------------------------------------------------------

関数の引数リストに真偽型の仮引数があるのは、コードの呼び出し側から見るとわかりに
くい。さらに、この手の関数は動作が高々二通りしかない。関数を将来的に拡張すること
が困難だろう。代替案として次を検討しろ：

* ``True``, ``False`` の場合それぞれの実装に作り直す。
* ``Enum`` を採用する。
* キーワード限定引数に変えて、実引数を与える際に呼び出し元が明示的に意味を示せる
  ようにする。

flake8-bugbear (B)
----------------------------------------------------------------------

プログラムのバグや設計上の問題を発見するための規則集とのことだ。雑多な項目からな
る。

* B002: C/C++ における ``operator++``, ``operator--`` に相当する演算子はない。
* B003: ``os.environ`` を左辺値のように扱うのはダメだ。
* B005: 文字列の ``strip`` 系メソッドに長さのある文字列を与えるのは誤り。
* B006: 関数の既定引数に mutable な値を指定するのはダメだ。
* B007: 未使用ループ変数は名前を ``_`` で始めろ。
* B{009,010}: ``getattr``, ``setattr`` よりも直接参照。
* B011: ``raise AssertionError`` は ``python -O`` の影響を受けないので ``assert
  False`` より良い。
* B012: ``finally`` 節で ``break``, ``continue``, ``return`` 文のいずれかを使う
  と例外が死んでしまう。
* B017: 例外を送出するためのテストにおいて ``BaseException`` や ``Exception`` を
  試すのはダメだ。もっと特殊な型を試せ。
* B019: メソッドに対して ``@functools.lru_cache`` や ``@functools.cache`` を使用
  するとメモリーリークを生じることがある。
* B021: docstring に f-string を使うのは誤り。その文字列が対象の ``__doc__`` と
  なることはない。
* B022: 趣旨とは外れるが ``contextlib.suppress`` は知らなんだ。
* B028: 関数 ``warnings.warn`` を呼ぶときには ``stacklevel=2`` かそれ以上が推奨。
* B034: 関数 ``re.sub``, ``re.subn``, ``re.split`` に ``count``, ``maxsplit``,
  ``flags`` を与えるときにはキーワード引数形式でなければダメだ。
* B901: ジェネレーターで ``return`` 文を書くのはダメだ。``StopIteration`` を送出
  したいのであっても、異なる書き方をしろ。
* B903: ``__init__`` しかないクラスはダメだ。``@dataclass`` 修飾を使うか
  ``collections.namedtuple`` にしろ。
* B904: ``except`` 節から別の例外を発生させる場合は ``from`` を使え。
* B{905,911}: 関数 ``zip``, ``batched`` にはキーワード引数 ``strict`` と値を明示
  しろ。

flake8-builtins (A)
----------------------------------------------------------------------

Python 組み込み型の名前をユーザーコードで変数などに割り当ててしまうのを避けたい。
例えば変数に ``max`` という名前を与えていないか、等。

flake8-commas (COM)
----------------------------------------------------------------------

* COM812: コレクションリテラルの CSV の最後の値のケツにもカンマを入れろ。
* COM818: 文末のカンマは誤りのはず。ほんとうに ``tuple`` リテラルを意図している
  のならば、丸括弧を明示的に書け。
* COM819: ``tuple`` リテラルの CSV の最後の値のケツにはカンマを入れるな。COM812
  と整合していないではないか。

flake8-copyright (CPY)
----------------------------------------------------------------------

これは面白い。コピーライト表記はあるべきだ。

* CPY001: Python ファイルの始めの方に Copyright 2025 xxxx のようなクレジット表記
  をしろ。

flake8-comprehensions (C4)
----------------------------------------------------------------------

内包記法に関する諸規則。

* C{400,401,416}: 冗長な ``x for x in y`` を書くな。
* C{403,404}: コンストラクター呼び出しではなく内包表記にしろ。
* C{405,406,408,418}: 冗長なコンストラクター呼び出しを書くな。
* C413: ``reversed(sorted(iterable))`` は効率が悪い。
* C415: ``reverse`` と ``sort`` を合成するな。
* C417: ``map`` を使うな。
* C419: 冗長なコレクション生成をするな。
* C420: ``dict.fromkeys(iterable)`` の存在を忘れるな。

flake8-datetimez (DTZ)
----------------------------------------------------------------------

クラス ``datetime.datetime`` に対する安心でない使用を禁止する規則集。特に、タイ
ムゾーン指定 ``tz``, ``tzinfo`` については必ず指定しろとある。

* DTZ001: ``datetime`` コンストラクターには ``tzinfo`` を与えろ。
* DTZ{002,003}: 関数 ``datetime.today``, ``datetime.utcnow`` はダメ。どちらの代
  わりにも 関数 ``datetime.now`` を使え。
* DTZ004: 関数 ``datetime.utcfromtimestamp`` ダメ。``datetime.fromtimestamp`` を
  ``tz`` 指定のうえ使え。
* DTZ{005,006}: 関数 ``datetime.now``, ``datetime.fromtimestamp`` は ``tz`` 指定
  必須。
* DTZ007: 関数 ``datetime.strptime`` を ``%z`` なしで使う場合には次のどちらかの
  呼び出しを続けろ：

  * ``.replace(tzinfo=)``
  * ``.astimezone()``
* DTZ011: 関数 ``date.today`` はダメ。``datetime.now(tz=).date()`` としろ。
* DTZ012: 関数 ``date.fromtimestamp`` はダメ。``datetime.fromtimestamp(,
  tz=).date()`` としろ。
* DTZ901: ``datetime.max``, ``datetime.min`` は使うなら ``.replace(tzinfo=)`` で
  作り直せ。

flake8-debugger (T10)
----------------------------------------------------------------------

リリースすることになっている Python ファイルにデバッガー起動処理が含まれているの
は意図せぬ状況であるはずだ。

* T100: ``breakpoint`` 呼び出しを入れたままにするな。

flake8-errmsg (EM)
----------------------------------------------------------------------

* EM101:	例外オブジェクトのコンストラクターに文字列リテラルを渡して ``raise`` す
  ると（一行で書くと）トレースバックが読みにくくなる。
* EM102	同じ状況で、f-string リテラルと値指定の組み合わせもダメ。
* EM103:	同じ状況で、文字列リテラルとメソッド ``format`` の組み合わせもダメ。

flake8-executable (EXE)
----------------------------------------------------------------------

Python ファイルの実行可能パーミッションと shebang が正しく設定されていることを保
証する。

* EXE001: Shebang を書くのならば ``chmod +x`` しておかねばならない。
* EXE002: 逆に、Python ファイルが実行形式ならば shebang がなければならない。
* EXE003: Shebang は :program:`python` のパスを指していなければならない。
* EXE005: Shebang はファイルの一行目になければならない。

flake8-future-annotations (FA)
----------------------------------------------------------------------

``from __future__ import annotations`` に関係する規則集。

* FA{100,102}: 型注釈をする場合にはこのインポート文が実質的に必須。修正挙動は構
  成要素 ``target-version`` の値が影響する。

flake8-implicit-str-concat (ISC)
----------------------------------------------------------------------

文字列リテラルの連結に関する規則集。

* ISC001: 文字列リテラル同士を空白で連結するのはダメだ。
* ISC{002,003}: 複数行にまたがる文字列はバックスラッシュや演算子 ``+`` で連結す
  るのではなく、丸括弧を用いた暗黙的連結法を採れ。

flake8-import-conventions (ICN)
----------------------------------------------------------------------

定番インポート文をまとめた規則集。

flake8-logging (LOG)
----------------------------------------------------------------------

* LOG001: ``Logger`` オブジェクトをコンストラクターから生成するのはダメだ。
* LOG002: ``logging.getLogger`` には ``__name__`` を渡せ。
* LOG007: ``logging.exception`` を ``exc_info=False`` で呼び出したければ、代わり
  に ``logging.error`` を呼べ。
* LOG009: ``logging.WARN`` ではなく ``logging.WARNING`` が正しい。
* LOG015: モジュール ``logging`` から ``debug``, ``info``, etc. を呼び出すことが
  可能ではあるが、それをするな。

flake8-logging-format (G)
----------------------------------------------------------------------

私が今までよく知らなかったログメッセージの書式整形について習得するための規則集。

* G001: ログ出力メソッド各種に実引数として渡す文字列で ``format`` をするのは効率
  が悪い。代わりに出力メソッドのキーワード引数 ``extra`` を上手く指定しろ。
* G{002..004}: 同じ理由により、いにしえの ``%`` 様式書式整形、文字列を連結するこ
  と、f-string を用いることのいずれもダメだ。
* G010: メソッド名は ``warn`` ではなく ``warning`` が正しい。
* G101: キーワード引数 ``extra`` のキーに次を使うな：

  * ``name``
  * ``level``
  * ``pathname``
  * ``lineno``
  * ``msg``
  * ``args``
  * ``exc_info``
  * ``func``
  * ``sinfo``
* G201: ``logging.error`` を ``exc_info=True`` で呼び出したければ、代わりに
  ``logging.exception`` を呼べ。
* G202: ``logging.exception`` 呼び出しでは ``exc_info=True`` は不要。

flake8-no-pep420 (INP)
----------------------------------------------------------------------

:file:`__init__.py` を持たない Python ファイルのディレクトリーがあるとする。これ
らは有効かつインポート可能だが、壊れるツールが存在する。

この手のディレクトリーは名前空間パッケージとして知られる特別なパッケージである場
合もあるが、名前空間パッケージはあまり広く使用されていない。したがって、通常の
パッケージが :file:`__init__.py` を備え忘れたものだと一般的にはみなされる。これ
を指摘する規則だ。

flake8-pie (PIE)
----------------------------------------------------------------------

いろいろな規則を寄せ集めたもの。

* PIE790: 不要な ``pass`` や ``...`` は削れ。
* PIE807: コンストラクター呼び出しで済むような ``lambda`` 式を書くな。

flake8-print (T20)
----------------------------------------------------------------------

* T{201,203}: 関数 ``print``, 関数 ``pprint.pprint`` を呼び出すのはダメだ。

flake8-pyi (PYI)
----------------------------------------------------------------------

型ヒント用ファイル (.pyi) 向け規則集。私はこのファイルを作らないので割愛。

flake8-pytest-style (PT)
----------------------------------------------------------------------

.. todo::

   Pytest は重要なパッケージ。ここも当然やる。

flake8-quotes (Q)
----------------------------------------------------------------------

* Q{000,001,002}:	二重引用符が望ましい。構成オプションによる。
* Q{003,004}:	文字列リテラル内側に引用符がある場合、外側の引用符と異なっているな
  らばエスケープは不要。

flake8-raise (RSE)
----------------------------------------------------------------------

* RSE102: 引数なしで例外を発生させる場合、``raise`` 文は例外オブジェクトの他に例
  外クラスを受け付ける。後者は暗黙的にオブジェクトを生成するので、コンストラク
  ター呼び出し括弧は必要ない。

flake8-return (RET)
----------------------------------------------------------------------

戻り値に関する規則集だ。

* RET501: 戻り値が ``None`` しかない関数内では ``None`` を明示的に返す書き方はダ
  メだ。単に ``return`` と書け。
* RET502: ``None`` でない値を返すことがある関数では ``None`` を暗黙的に返すのは
  ダメだ。``return None`` と書け。
* RET503: RET502 と同じ仮定で、関数の最後に ``return`` を明示しろ。
* RET504: 代入された変数の ``return`` を行うまさに直前に、その代入があるのはダメ
  だ。代入文を削って、その右辺と同じものを返せ。
* RET{505..508}: ``return`` 文や ``raise`` 文や ``continue`` 文や ``break`` 文を
  含む ``if`` 節に ``else`` 節もあるのはダメだ。

flake8-self (SLF)
----------------------------------------------------------------------

* SLF001: アンダースコアから始まるような名前であるクラスメンバーに外部からアクセ
  スしてはいけない。

flake8-slots (SLOT)
----------------------------------------------------------------------

余計なメモリーを食わぬように、immutable 型の派生クラス定義では ``__slots__`` の
定義を空にしろという規則だ。基底クラスが次のいずれかである場合に適用する：

* SLOT000: ``str``
* SLOT001: ``tuple``
* SLOT002: ``collections.namedtuple``, ``typing.NamedTuple``

flake8-simplify (SIM)
----------------------------------------------------------------------

コードを単純なままに保つための規則集。これは重要。

* SIM101: 関数 ``isinstance`` は引数に型を複数取れる。
* SIM102: 入れ子の ``if`` 文を平たく書き直せるならそうしろ。
* SIM103: ``return`` 文で済むような ``if`` ブロックを書くな。
* SIM105:	``contextlib.suppress`` で済ませたい例外ブロックがないか？
* SIM107:	``finally`` 節に ``return`` 文を書いてはいけない。
* SIM108:	三項演算子や二項演算 ``or`` で済む ``if``-``else`` ブロックを書くな。
* SIM109:	オブジェクトが複数対象のいずれかと等しいかどうかを調べるには演算子
  ``in`` を使え。
* SIM110:	組み込み関数 ``all``, ``any`` のような処理を手で書くな。
* SIM115:	ファイルを開く関数を呼ぶときには ``with`` 文を使え。
* SIM116:	ある種の ``if`` 文連続は辞書オブジェクトアクセスに置き換えろ。
* SIM117:	入れ子の ``with`` 文は ``as`` 節をカンマ区切りで書くことで平たくしろ。
* SIM118: 辞書メソッド ``keys`` 呼び出しを ``in`` の右側に書くな。
* SIM210:	値が ``True`` か ``False`` になる三項演算子呼び出しは ``bool`` 変換に
  書き換えろ。
* SIM211:	SIM 210 の裏。オペランドを演算子 ``not`` に作用させろ。
* SIM212:	三項演算子を ``if not`` の形で使うな。
* SIM{222,223}:	truthy/falsey な値を複数 ``or``/``and`` で連結するな。
* SIM300: ``==`` の左辺に定数を置いた条件文は Python でなくてもダサい。
* SIM401:	辞書メソッド ``get`` で済む処理を ``if`` で書くな。
* SIM905:	リストリテラルで置き換えられる内容を文字列メソッド ``split`` の呼び出
  しで済ますな。
* SIM910:	辞書メソッド ``get`` の呼び出しでは第二引数に ``None`` を書くな。
* SIM911:	辞書の ``keys`` と ``values`` を ``zip`` するな。それは ``items`` だ。

flake8-tidy-imports (TID)
----------------------------------------------------------------------

インポート文は整然としていなければダメだ。

* TID252: 相対インポートは兄弟からの相対インポートでなければダメだ。
* TID253: インポートが重いモジュールについては、最上位スコープからインポートする
  のはダメだ。型注釈にしか用いないものをインポートするときには専用 ``if`` 文でし
  ろ。

flake8-type-checking (TC)
----------------------------------------------------------------------

型注釈をする場合、次のような定型コードを書く。この ``if`` ブロックを型検査ブロッ
クと呼ぶことにする。TC は型検査ブロックに関する規則集だ。

.. sourcecode:: python
   :caption: 型検査ブロックコード
   :force:

   from __future__ import annotations
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       ...

* TC{001..003}: 型検査にしか用いない型をインポートする場所が型検査ブロックでない
  のはダメだ。
* TC004: 逆に、実行時機能として用いるものは型検査ブロック外でインポートする必要
  がある。
* TC005: 空の型検査ブロックは不要。
* TC006: 関数 ``typing.cast`` 呼び出しの第一引数は型そのものではなく、文字列で指
  定しろ。
* TC007: 明示的な ``TypeAlias`` において、実行時に利用できないシンボルへの参照が
  含まれていてはいけない。これも文字列で指定しろ。
* TC008: 逆に、文字列ではなく型そのもので別名を与えろ。
* TC010: ``X | Y`` 式の型注釈において、型そのものと文字列を混在してはダメだ。

flake8-unused-arguments (ARG)
----------------------------------------------------------------------

関数定義で未使用の仮引数があるのはダメだ。

* ARG{001..004}: サブクラスのメソッド実装などでそのような引数が生じる場合には、
  変数名の頭に ``_`` を付けてしのげ。
* ARG005: ラムダ式でも同様にしろ。

flake8-use-pathlib (PTH)
----------------------------------------------------------------------

標準モジュール ``pathlib`` の機能で代替可能な旧式コードを置換しろという規則集だ。
標準モジュール ``os``, ``os.path`` のコードが該当しがちだ。

* PTH123: 組み込み関数 ``open`` 呼び出しをクラス ``Path`` のメソッド ``open`` に
  なるべく置き換えろ。
* PTH201: ``Path(".")`` ではなく ``Path()`` でよい。
* PTH207: 標準モジュール ``glob`` の関数 ``glob``, ``iglob`` 呼び出しを ``Path``
  のメソッド ``glob``, ``rglob`` で置き換えろ。
* PTH210: メソッド ``with_suffix()`` の実引数はドット始まりでなければならない。

flake8-todos (TD)
----------------------------------------------------------------------

TODO コメント規則集。

* TD001: ``FIXME`` や ``XXX`` ではなく ``TODO`` と書け。
* TD002:	``TODO`` に署名をしろ。例えば ``TODO(someone)`` のように。
* TD003:	TODO コメントに関連する URL を書け。
* TD004:	``TODO`` タグは ``:`` で終われ。
* TD005:	TODO コメントに記述がないのではダメだ。
* TD006:	``TODO`` は全文字大文字で書け。
* TD007:	``TODO(someone):`` のコロンの次の文字は空白にしろ。

flake8-fixme (FIX)
----------------------------------------------------------------------

* FIX{001..004}: ``FIXME``, ``TODO``, ``XXX``, ``HACK`` コメントが残っている。問
  題に対処してからコメントを消せ。

eradicate (ERA)
----------------------------------------------------------------------

Python ファイルからコメントアウトされたコードを削ることで知られるプログラムの名
を冠した規則だ。

pygrep-hooks (PGH)
----------------------------------------------------------------------

* PGH003: ``type: ignore`` コメントでは何を無視するのかを書け。
* PGH004: ``noqa`` コメントには規則番号を付けろ。
* PGH005: invalid-mock-access	Mock method should be called: {name}	✔️ 🛠️

Pylint (PL)
----------------------------------------------------------------------

Pylint はこの分野の老舗だ。違反区分として Convention, Error, Refactor, Warning
を設けている。Ruff_ ではそれぞれに PLC, PLE, PLR, PLW の接頭辞を割り当てている。

* PLC{0105,0131}: この記述が理解できぬ場合には PEP483_ を熟読しろ。
* PLC0206: 辞書を反復するにはメソッド ``items()`` を明示しろとある。
* PLC0208: リテラル集合を反復するのはダメだ。
* PLC0415: ``import`` 文はよほどのことがない限りスコープの最上位にしか書かない。
* PLC2801: 二重アンダースコアメソッドを明示的に呼び出すのはダメだ。対応するメ
  ソッドを呼べ。
* PLE0115: ``global`` かつ ``nonlocal`` である変数はそもそも論理的に矛盾している。
* PLE0116: ``continue`` 文を ``finally`` 節に書くのは現在は ``SyntaxError`` 送出。
* PLE{0604,0605}: ``__all__`` の値は文字列からなる ``list`` または ``tuple`` と
  する。
* PLE1132: キーワード引数で同一キーの実引数を指定するのはダメだ。
* PLE1141: なぜ辞書を反復するのにメソッド ``items()`` を明示するべきなのかの解説
  がある。キーが特定の型の値である場合にマズイことになる。
* PLE1700: ``async for`` 文が必要になる場合。
* PLE4073: 集合オブジェクトの内容を in-place で変更する場合があれば、コピーオブ
  ジェクトを反復せざるを得ない。
* PLR0124: コード中に ``x == x`` のようなテストがあれば、それは ``x`` が NaN で
  あるかをテストしていると考えられる。
* PLR0133: 定数同士を実行時に比較するな。
* PLR{0202,0203}: デコレーターとして供給されている関数はデコレーターとして使え。
* PLR0904: この規則は邪魔だ。メソッドがたくさんあってもいいではないか。
* PLR0917: キーワード限定引数を上手く使いこなせ。関数定義の引数リストの書き方を
  習得しろ。
* PLR1733: ``FRUITS.values()`` を反復するという解法もある。PLR1736 も同様。
* PLR2004: これも邪魔だ。この規則のいう common values では間に合っていない。
* PLR5501: Python ``elif`` はよく忘れる。
* PLR6104: この手の代入演算を augmented assignment と呼ぶのは知らなんだ。
* PLR6201: ``in [...]`` などよりは ``in {...}`` のほうが望ましい。
* PLW0133: 例外オブジェクトを ``raise`` なしに構築することはない。
* PLW0177: NaN 判定は ``math.isnan`` か ``np.isnan`` を使え。直接比較をするな。
* PLW1510: 関数 ``subprocess.run`` には ``check=True`` を与えろ。
* PLW1514: テキストファイルを ``open`` するときには ``encoding="utf-8"`` を（わ
  かっていても）付けろ。
* PLW1641: ``__eq__`` を実装するときには ``__hash__`` も実装しろ。
* PLW3301: 関数 ``min`` や ``max`` の呼び出しを入れ子にするな。

tryceratops (TRY)
----------------------------------------------------------------------

   A linter to prevent exception handling antipatterns in Python (limited only
   for those who like dinosaurs). (About, GitHub guilatrova/tryceratops)

* TRY002: 超基本だが ``Exception`` そのものを送出してはいけない。
* TRY003: 例外文言は自作した例外クラスの中で組み立てられるように設計しろ。
* TRY004: ``TypeError`` と ``ValueError`` のどちらにも取れる状況では前者を送出し
  ろ。
* TRY201: 処理ブロックから再送出する場合には ``raise`` に引数を付けない。
* TRY203: 再送出しかしない ``except`` 節は不要。
* TRY300: ``try`` 節で ``return`` 文を書きたい場合、そうはせずに ``else`` 節を設
  けてそこに置け。
* TRY301: ``try`` 節に内部関数を定義する場合、その戻り値に基づいた ``raise`` 文
  を書くのはダメ。
* TRY{400,401}: 関数 ``logging.exception`` を上手く使え。要練習。

flynt (FLY)
----------------------------------------------------------------------

* FLY002: f-string で書ける文字列 ``join`` はダメだ。

NumPy-specific rules (NPY)
----------------------------------------------------------------------

:doc:`NumPy </python-numpy/index>` を使うときにオンにする規則集。

* NPY001: ``np.int`` などの型別名は一部の除外対象を除き使用不可。単に ``int`` な
  どに書き換えろ。
* NPY002: ``np.random`` の関数のうち、旧式のものを使用してはダメだ。
* NPY003: NumPy が deprecated だと認定しているインターフェイスを使用してはいけな
  い。
* NPY201: numpy2-deprecation

refurb (FURB)
----------------------------------------------------------------------

ここは耳が痛い規則が多い。

* FURB{101,103}: 組み込み関数 ``open`` からの ``read``/``write`` はダサい。クラ
  ス ``pathlib.Path`` の機能を使え。
* FURB110: ``x if x else y`` は ``x or y`` で十分。やらかしていそうで怖い。
* FURB132: 組み込み型 ``set`` にはメソッド ``discard`` がある。
* FURB136: ところで Python には minmax 関数がない？
* FURB142: 集合演算のメソッド名は思い出しにくい。
* FURB145: ``a[:]`` よりも ``a.copy()`` のほうが望ましいとある。
* FURB148: Sequence を反復するときにインデックスしか要らない場合には
  ``range(len(x))`` を用いるのが望ましい。
* FURB161: 整数メソッド ``bit_count`` はいずれ使う可能性がある。
* FURB163: 特殊な底の対数関数は効率や精度が優れた特別版 (e.g. ``log10``) がある。
* FURB166: {2,8,16} 進数を表す文字列を手動で処理していないか。やらかしている可能
  性が高い。
* FURB167: ``re.I`` などは ``re.IGNORECASE`` などと書かないようではダメだ。
* FURB181: メソッド ``hexdigest`` の使用推奨。確認したら大丈夫だった。
* FURB188: メソッド ``removeprefix``, ``removesuffix`` は使った記憶がない。

Ruff-specific rules (RUF)
----------------------------------------------------------------------

* RUF{001..003}: 日本語混じりのテキストを扱うときにこの規則が邪魔になるか？
* RUF005: Sequence を連結する unpacking の手筋。
* RUF007: 関数 ``itertools.pairwise`` は知らなんだ。連続する要素の対を反復する。
* RUF015: ``next(iter(x))`` 手筋。これを指摘されて Ruff に興味を持ったのだった。
* RUF017: 入れ子になったリストを quadratic list と呼んでいる。
* RUF029: なぜかこれをやらかしがちだ。そういう粗忽者は自分だけではないのか。
* RUF031: ``tuple`` がキーであるようなコレクションの要素アクセス。知らなんだ。
* RUF032: ``Decimal(1.2345)`` はダメ。``Decimal("1.2345")`` のように書け。
* RUF034: FURB110 と同類の規則。
* RUF036: 型ヒントの union では ``None`` を最後に書け。
* RUF039: 正規表現関数には必ず生文字列を渡せ。
* RUF048: バージョン文字列 ``__version__`` は関数 ``packaging.version.parse`` に
  通じる値でなければならない。
* RUF055: 単純な文字列操作をするのに正規表現操作を適用するのはダメだ。

資料集
======================================================================

Ruff_
   公式文書。
`Ruff - Visual Studio Marketplace <https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`__
   EXTENSIONS パネルの検索欄で Ruff と入力すると現れる。
`lint - What is "Linting"? <https://stackoverflow.com/questions/8503559/what-is-linting>`__
   Stack Overflow 内の質疑応答スレ。
`Action Comments - isort <https://pycqa.github.io/isort/docs/configuration/action_comments.html#isort-off>`__
   :samp:`# isort: {directive}` 系コメント指令の仕様はこれに由来する。
`How can I print to standard output what rules are currently enabled given my config? <https://github.com/astral-sh/ruff/discussions/8724>`__
   GitHub リポジトリーより。

.. include:: /_include/python-refs-core.txt
.. _PEP483: https://peps.python.org/pep-0483/
.. _pre-commit: https://pre-commit.com/
.. _Ruff: https://docs.astral.sh/ruff/
