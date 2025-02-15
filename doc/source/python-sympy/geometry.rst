======================================================================
幾何
======================================================================

SymPy_ のサブパッケージ ``sympy.geometry`` に関わる覚え書きを記す。

.. contents:: ノート目次

主要クラス図
======================================================================

サブパッケージ ``sympy.geometry`` が提供する主要クラスの継承関係のみを図示すると
こういう感じになる。

.. mermaid::

   classDiagram
       GeometryEntity <|-- Point
       GeometryEntity <|-- Point3D
       GeometryEntity <|-- LinearEntity
           LinearEntity <|-- Segment
           LinearEntity <|-- Ray
           LinearEntity <|-- Line
       GeometryEntity <|-- LinearEntity3D
           LinearEntity3D <|-- Line3D
           LinearEntity3D <|-- Ray3D
           LinearEntity3D <|-- Segment3D
       GeometryEntity <|-- Plane
       GeometryEntity <|-- Polygon
           Polygon <|-- Triangle
           Polygon <|-- RegularPolygon
       GeometryEntity <|-- Ellipse
           Ellipse <|-- Circle
       GeometryEntity <|-- Curve

* クラス ``GeometryEntity`` のスーパークラスはクラス ``Basic`` である。

クラス継承関係
======================================================================

* 基本的に二次元幾何。同じ幾何要素で次元が異なるものはクラスも別々に定義があ
  る。例えば ``Point`` と ``Point3D`` が存在する。

  * ここにあるあらゆるメソッド、関数は 2D と 3D を混ぜて利用することを想定してい
    ない。

* ``RegularPolygon`` is-a ``Polygon`` だったり ``Circle`` is-a ``Ellipse`` だっ
  たりする。オブジェクト指向プログラミングの本からするとこういう設計はするなと言
  われそうだが、SymPy は記号数学のライブラリーなのでむしろアリということだろう。

共通機能
======================================================================

ここでは便宜上、次のものを共通機能と呼んで理解を深める。

#. クラス ``GeometryEntity`` のオブジェクトを引数に取る関数
#. クラス ``GeometryEntity`` の静的・クラスメソッド
#. クラス ``GeometryEntity`` のメソッド

クラス ``GeometryEntity`` のオブジェクトを引数に取る関数
----------------------------------------------------------------------

* 関数 ``intersection``

  * 引数は複数個の ``GeometryEntity`` オブジェクト。
  * 戻り値は ``list`` で、その要素は ``Point`` や ``Segment`` になるのだろう。

* 関数 ``convex_hull``

  * 複数個の ``Point``, ``Segment``, ``Polygon`` オブジェクトを引数に取る。
  * 戻り値は基本的には凸包を表現する ``Polygon`` オブジェクトだが、場合によって
    は ``Segment`` かもしれない。

* 関数 ``are_coplanar``

  * 引数は複数個の ``GeometryEntity`` オブジェクト。
  * 引数のすべての 3D オブジェクト全部がある平面上に乗っているかどうかをテストす
    る。
  * そのような平面が ``Plane`` オブジェクトとして返るわけではないようだ？
  * 2D のオブジェクトは一応 3D 化してから計算してくれる。計算するまでもないだろ
    う。

* 関数 ``are_similar``

  * ふたつの ``GeometryEntity`` オブジェクトが相似かどうかをテストする。
  * 単に :code:`entity1.is_similar(entity2)` よりも気が利いた処理をするに過ぎな
    い。

* 関数 ``centroid``

  * 引数は複数個の ``GeometryEntity`` オブジェクト。
  * おそらく同型でなければならない。
  * 戻り値は ``Point`` オブジェクトで、オブジェクト全部が決定する重心の座標を表
    現する。

クラス ``GeometryEntity`` の静的・クラスメソッド
----------------------------------------------------------------------

クラス ``GeometryEntity`` の静的・クラスメソッドは存在しない。

クラス ``GeometryEntity`` のメソッド
----------------------------------------------------------------------

* メソッド ``intersection`` は先述の同名関数を参照。
* メソッド ``is_similar`` は先述の関数 ``are_similar`` を参照。
* 変形系メソッド ``rotate``, ``scale``, ``translate``, ``reflect`` が提供されて
  いる。

  * ``rotate``, ``scale`` は変形の原点を指定できる。
  * ``reflect`` には ``LinearEntity`` オブジェクトを渡すようだ。

* メソッド ``encloses``

  * 自身のオブジェクトの内側に与えられたオブジェクト全体を含むかどうかをテストす
    る。
  * 実装にはサブクラスのメソッド ``encloses_point`` を利用している。
  * 造りが美しくない。

* メソッド ``equals`` が提供されており、オーバーライドがなければ :code:`e1 ==
  e2` と同値。
* 演算子がいくつか定義されているが、これらの存在はひとまず忘れておく。

サブクラス
======================================================================

以下、クラス ``GeometryEntity`` の各サブクラスについての感想やら何やらを記す。

* クラス ``Point``

  * 座標成分は具体的な数値でもよいし、シンボルでもよい。ただし、いくつかの判定モ
    ノの関数は具体的な ``Point`` で計算しないと意味がなくなる。

  * プロパティー ``length`` は必ずゼロを返す。
  * メソッド ``is_collinear`` と ``is_concyclic`` はクラスメソッドである。

   * 類似したライブラリーを色々知っているが ``is_concyclic`` 的なものは初めてお
     目にかかる。

  * メソッド ``evalf`` は各座標を浮動小数点数で表現し直した ``Point`` を返す。
  * メソッド ``dot`` でドット積を計算する。
  * 演算子で加算、減算、スカラー倍、etc. が実現できる。
    単項マイナスと絶対値もサポート。

  * メソッド ``transform`` は行列を右から掛けるようだ。vM 方式。

* クラス ``Point3D``

  * クラス ``Point`` にあるものは、だいたいその三次元版メンバーが存在する。
  * クラス ``Point`` にはない次のメソッドに注意。

    * メソッド ``direction_ratio``, ``direction_cosine``
    * クラスメソッド ``are_collinear``, ``are_coplanar``

  * メソッド ``is_collinear`` と ``is_concyclic`` は存在しない。

* クラス ``LinearEntity``

  * 二次元空間内のまっすぐな線のためのスーパークラス。
  * この手のクラスによくあるプロパティー、メソッドがやはりある。
  * メソッド ``parallel_line``, ``perpendicular_line`` は ``Line`` オブジェクト
    を生成する。

    * 一方、メソッド ``perpendicular_segment`` は ``Segment`` オブジェクトを生成
      する。

  * クラスメソッド ``are_concurrent`` 的なものは初めてお目にかかる。すべての引数
    が「一点で交差する」かどうかをテストする。
  * メソッド ``intersection`` の対象は ``Point`` か ``LinearEntity`` に限定して
    いる？
  * メソッド ``arbitrary_point`` で線上の任意の一点を返す。

    * デフォルトでは線のパラメーターシンボルを ``t`` とする。

  * メソッド ``random_point`` で線上の勝手な一点を返す。
  * メソッド ``is_similar`` は線の傾きを比較する。
  * メソッド ``contains`` は形状を集合と見たときの包含関係のテストと思ってよい。
  * メソッド ``distance`` はここにはなく、各サブクラスにある。

* クラス ``Segment``

  * 有限の線分を表現する。
  * メソッド ``plot_interval`` は :code:`list(t, 0, 1)` を返す。
  * メソッド ``perpendicular_bisector`` の仕様が CAD の感覚だとやや不親切な気が
    する。指定点が bisector に乗らない場合は、直線ではなくて中点から投影点までの
    線分を生成するのかと思った。

* クラス ``Ray``

  * 半直線を表現する。
  * メソッド ``plot_interval`` は :code:`list(t, 0, 10)` を返す。
  * プロパティー ``xdirection``, ``ydirection`` により、形状がどの座標軸に沿って
    無限なのかがわかる。

* クラス ``Line``

  * 直線を表現する。
  * メソッド ``plot_interval`` は :code:`list(t, -5, 5)` を返す。
  * こいつだけメソッド ``equation`` を持っていて、直線の式 :code:`simplify(a*x +
    b*y + c)` を生成する。

* クラス ``LinearEntity3D`` およびそのサブクラス群が ``LinearEntity`` 系と同じ階
  層構造で存在する。
* クラス ``Plane``

  * 平面を表現する。平面に期待するメンバーが存在する。
  * 平行、垂直のテストは ``LinearEntity3D`` または ``Plane`` に対するものだ。
  * メソッド ``distance`` の対象は ``Point3D``, ``LinearEntity3D`` または
    ``Plane`` のいずれか。
  * メソッド ``arbitrary_point``, ``random_point`` がある。
  * クラスメソッド ``are_concurrent`` は複数の平面が共通の直線で交わるかどうかを
    テストする珍しいものだ。
  * メソッド ``is_coplanar`` で平面に乗るかどうかをテスト。

* クラス ``Polygon``

  * xy 平面上の多角形を表現する。
  * コンストラクターが気を利かせて、別のクラスのオブジェクトを生成することがあ
    る。極端な例を挙げると、一直線上に並ぶ任意の点列を ``Polygon`` のコンストラ
    クターに与えると、得られるオブジェクトの型はなんと ``Segment`` である。

  * プロパティー ``area`` で面積を計算する。符号付きの可能性がある。
  * プロパティー ``angles`` で内角の ``list`` を返す。
  * プロパティー ``perimeter`` は周長を返す。
  * プロパティー ``centroid`` で重心に位置する ``Point`` オブジェクトを生成す
    る。
  * プロパティー ``sides`` で各辺を ``Segment`` で表現するオブジェクトの
    ``list`` を返す。

    * メソッド ``intersection`` の計算はこれに基づく。

  * メソッド ``is_convex`` でこの多角形が凸かどうかをテストする。
  * メソッド ``arbitrary_point`` について

    * :code:`t=0` で始点
    * :code:`t=1` で終点

  * メソッド ``plot_interval`` は :code:`list(t, 0, 1)` を返す。

* クラス ``Triangle``

  * 三角形は多角形の中でも別格の存在ということで、専用クラスとして存在するよう
    だ。
  * コンストラクターは色々な引数指定をサポートしている。使いやすいものを覚えてお
    くこと。

    * 単に三頂点を ``Point`` オブジェクトで指定する。
    * キーワード引数 ``sss`` 等と辺の長さ・角度を列挙を組み合わせて指定する。

      * オブジェクトの座標があらかじめ想像しづらい。

  * メソッド ``is_similar`` の実装は、三辺の比をテストするだけ。辺の順序の組み合
    わせはすべて考慮する。

  * メソッド ``is_equilateral`` で正三角形テスト。
  * メソッド ``is_isosceles`` で二等辺三角形テスト。
  * メソッド ``is_right`` で直角三角形テスト。

  * 五心

    .. csv-table::
       :delim: @
       :header-rows: 1
       :widths: auto

       名前 @ Point @ Circle @ 何の交点か
       外心 (O) @ ``circumcenter`` @ ``circumcircle`` @ :code:`sides().perpendicular_bisector()`
       垂心 (H) @ ``orthocenter`` @ なし @ ``altitudes``
       内心 (I) @ ``incenter`` @ ``incircle`` @ ``bisectors``
       傍心 (J) @ なし @ なし @ なし
       重心 (G) @ ``centroid``@ なし @ ``medians``

* クラス ``RegularPolygon``

  * 正多角形を表現するクラス。
  * 頂点の位置を直接指定してオブジェクトを生成するというよりは、半径と頂点数を指
    定する。
  * プロパティー ``length`` の実装を見ると非効率的な印象を受けるが、記号数学演算
    的にはこれしかない。

    * これは ``perimeter`` を利用しない。

  * プロパティー ``apothem`` および ``inradius`` で内接円の半径を得る。
  * プロパティー ``interior_angle`` と ``exterior_angle`` で多角形の内角、外角を
    それぞれ得る。
  * プロパティー ``incircle`` と ``circumcircle`` で内接円、外接円を Circle オブ
    ジェクトとしてそれぞれ得る。

  * コンストラクターおよびメソッド ``spin`` で多角形の中心点を軸に回転をかけられ
    る。

* クラス ``Ellipse``

  * コンストラクターが色々ある。

    * 長軸・短軸ではなく ``hradius``, ``vradius`` のような扱いをする。

  * プロパティー ``minor``, ``major`` で長軸、短軸の半分の長さを得る。
  * プロパティー ``circumference`` で楕円の周長が得られる。定積分オブジェクトか
    もしれない。
  * プロパティー ``periapsis``, ``apoapsis`` で楕円の焦点から近点、焦点から遠点
    の距離がそれぞれ得られる。

  * メソッド ``tangent_lines`` である点から楕円上に接線を求める。

    * たいていの場合、戻り値は ``Line`` オブジェクト二個の ``list`` となる。

  * メソッド ``is_tangent`` は ``Ellipse`` にも対応している。
  * メソッド ``normal_lines`` はある点から楕円に垂直に交差する ``Line`` を求め
    る。

    * 要素数は 1, 2, 4 のいずれか。
    * キーワード引数 ``prec`` の存在に注意。

  * メソッド ``plot_interval`` は :code:`list(t, -S.Pi, S.Pi)` を返す。
  * メソッド ``equation`` で楕円の方程式（の左辺）を得る。
  * メソッド ``evolute`` で楕円の縮閉線の方程式（の左辺）を得る。

* クラス ``Circle``

  * コンストラクターは次のどちらかの引数リストを受け付ける。

    * 通過点を表現する ``Point`` オブジェクト三つ。
    * 中心を表現する ``Point`` と半径。

  * メソッド ``scale`` で ``Ellipse`` オブジェクトが生成することがある。

* クラス ``Curve``

  * 平面的なパラメトリック曲線を表現するクラス。
  * コンストラクターの例： :code:`Curve((sin(t), cos(t)), (t, 0, 2))`
  * プロパティー

    * ``limits`` は曲線のパラメーター定義域を表現する ``tuple`` である。
    * ``parameter`` は曲線のパラメーターのためのシンボルである。
    * ``functions`` は各座標成分の関数の ``tuple`` である。

デモ
======================================================================

メネラウスの定理
----------------------------------------------------------------------

.. literalinclude:: /_sample/sympy/menelaus.py
   :language: python3

* 本当は数値的でないほうの座標で検証したかったが、私の環境では
  :code:`simplify(numer/denom)` が返って来なかった。
* 具体的な座標を与えた方の検証はうまくいく。

  .. code:: console

     bash$ ./menelaous.py
     P= Point(-346.683333333333, -346.683333333333)
     Q= Point(170.682926829268, 170.682926829268)
     R= Point(-241.237623762376, -241.237623762376)
     numer= 41999675.9784931
     denom= 41999675.9784931
     1.00000000000000

チェバの定理
----------------------------------------------------------------------

.. literalinclude:: /_sample/sympy/ceva.py
   :language: python3

* 本当は数値的でないほうの座標で検証したかったが、私の環境では
  :code:`simplify(numer/denom)` が返って来なかった。
* 具体的な座標を与えた方の検証はうまくいく。

  .. code:: console

     bash$ ./ceva.py
     P= Point(13.9279086822051, 228.152408889456)
     Q= Point(280.783950617284, 43.1975308641975)
     R= Point(104.14656234152, 529.558791567051)
     numer= 20374326.3842940
     denom= 20374326.3842940
     1.00000000000000

方べきの定理
----------------------------------------------------------------------

具体的な座標を与えないとどうも上手くいかないようなので、数値計算に切り替えて様子
見だ。さらに難易度？を落とし、方べきの定理を再現してみたい。

.. literalinclude:: /_sample/sympy/circle_power.py
   :language: python3

円を単位円に固定する代わり、円周上の四点をランダムにとり、それらを結ぶ二弦の交点
に対する方べきの定理を検証しよう。

.. code:: console

   bash$ ./circle_power.py
   PA * PB = 0.245325501000245
   PC * PD = 0.245325501000245
   bash$ ./circle_power.py
   PA * PB = 0.0519999915840500
   PC * PD = 0.0519999915840500

----

.. todo::

   * プロットは実現したい。
   * 上の例で ``distance`` を多用しているが、値一致テストの目的なら ``dot`` を用
     いるのが常識的か。
   * もっとサンプルを作りたい。

.. include:: /_include/python-refs-core.txt
.. include:: /_include/python-refs-sci.txt
