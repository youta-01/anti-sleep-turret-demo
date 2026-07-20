# ADR 003: 例外を明示的なモードにする

## Context

強制介入だけでは、通話、試験、休憩、障害対応など正当な中断理由を扱えません。一方、無条件停止は通常回避に使われ得ます。

## Decision

Daily Rest、Call Safe Mode、Exam Mode、Emergency Safe Modeを、条件と終了挙動を持つ明示的な状態として扱います。

## Alternatives

- いつでも停止できる共通ボタン
- 例外を一切設けない
- 状況を自動推定して暗黙に停止する

## Trade-offs

継続利用しやすくなる一方、ポリシーが複雑になり、例外間の競合テストが必要です。

## Observed consequence

回数制限、終了後猶予、Bath要求、Riz中の制約を決定的テストで表現できました。

## Current status

採用中。Emergency Safe Modeは外部のTechnical Safety Cutoffの代わりではありません。
