# ADR 002: 介入を段階化する

## Context

弱い兆候と強い兆候を同じ強制で扱うと、不要な負担が増えます。

## Decision

MONITORING、LV1_WARNING、LV2_WARNINGを経て、Lv3または反復リスクでBATH_REQUIREDへ進む段階的介入を採用します。

## Alternatives

- 最初の兆候で直ちにBathを要求する
- 警告だけで強制状態を持たない
- 連続値だけを表示し状態を持たない

## Trade-offs

状態数とテスト項目は増えますが、介入の意味と遷移理由が明示できます。

## Observed consequence

合成シナリオで軽度警告、強警告、直接Bath、信号解消を独立に再現できました。

## Current status

公開デモと現行標準フローで採用中。閾値は科学的精度の主張ではありません。
