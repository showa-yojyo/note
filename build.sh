#!/bin/bash
# $Id$

RST2HTML=./rst2html.py
CSSFILE=./note.css
DEST=./build

# build ��̃f�B���N�g�����m��
mkdir -p ${DEST}

# rst2html �R���o�[�g
for SOURCE in *.txt ; do
  TARGET="${SOURCE%%.txt}.html"
  if [ "$SOURCE" -nt "$DEST/$TARGET" ] ; then
    echo Processing $SOURCE...
    "$RST2HTML" "$SOURCE" "$DEST/$TARGET"
  fi
done

# css �t�@�C���� build ��f�B���N�g���փR�s�[
if [ -f "$CSSFILE" ]; then
  cp -u note.css ${DEST}
fi
