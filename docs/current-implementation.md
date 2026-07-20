# 現在の公開実装

## リスク計算

公開デモの合成入力は `eye_closed_seconds`、`head_down_seconds`、`face_missing_seconds` の3つです。各値をLv3閾値（90秒、1200秒、1200秒）で正規化し、最大値を0〜100の Sleep Risk とします。有効な入力がひとつもない場合は検出不能として扱います。

| 入力 | Lv1 | Lv2 | Lv3 |
| --- | ---: | ---: | ---: |
| Eye Closed | 20秒 | 45秒 | 90秒 |
| Head Down | 300秒 | 600秒 | 1200秒 |
| Face Missing | 600秒 | 900秒 | 1200秒 |

Risk 50以上への到達を1 episodeとして数え、Risk 35以下が15秒続くと再アームします。60分以内に3 episodeが成立すると `BATH_REQUIRED` へ進みます。

## Bathと例外

強制BathはStart QR後8〜15分、Manual Bathは5〜45分です。強制Bathでは開始15秒後からPresence Guardが有効になり、顔または十分な動きを検出すると開始を無効化して `BATH_REQUIRED` に戻します。Rizは独立状態ではなく、Bathへの介入元とオレンジ色の表示文脈です。

Daily Rest、Call Safe Mode、Exam Mode、Emergency Safe Modeは、通常利用を継続するための明示的な例外です。Technical Safety Cutoffはこの公開デモでは文書化のみで、状態機械の外側にあります。

詳しくは [状態遷移](state-transitions.md) と [BathとRiz](bath-and-riz.md) を参照してください。
