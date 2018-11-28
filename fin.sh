#!/usr/bin/env bash

  curl -s 'https://marknadssok.fi.se/publiceringsklient/' 'Accept-Encoding: gzip, deflate, br' |
  ggrep -E '<td>|Detaljer'|
  ggrep -v '<td>Ja</td>'|
  head -16 |
  sed 's/^[ \t]*//;s/.*<td>//;s/<\/td>.*//;s/<a href="//;s/>Detaljer<\/a>.*//;s/"//;/^[[:space:]]*$/d'|
  grep -v '2018' |
  grep -v 'SE00' |
  python3 -c 'import html, sys; [print(html.unescape(l), end="") for l in sys.stdin]' > insyn.txt
