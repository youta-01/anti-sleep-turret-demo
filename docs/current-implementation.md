# 現在の公開実装

## リスク計算

合成入力は `eye_closed_seconds`、`head_down_seconds`、`face_missing_seconds` の3つです。各値をLv3閾値（90秒、1200秒、1200秒）で正規化し、最大値を0–100に制限して Sleep Risk とします。利用可能な入力が一つもない場合は検知不能として扱います。

Lv1/Lv2/Lv3の閾値は、閉眼が20/45/90秒、頭部下降が300/600/1200秒、顔不在が600/900/1200秒です。Risk 50以上の連続期間は1エピソードとして数えます。Risk 35以下が15秒連続すると再アームし、60分以内に3回発生すると入浴必須になります。

## 通常の強制入浴

有効な流れは次のとおりです。

```text
MONITORING → LV1_WARNING または LV2_WARNING → BATH_REQUIRED
→ Start QR合成イベント → BATH_STARTED
→ 有効時間後のComplete QR合成イベント → MONITORING
```

完了可能時間は開始後8分から15分までです。8分未満の完了は拒否され、15分超過は `BATH_TIMEOUT` になります。タイムアウト後は新しいStartイベントが必要です。完了後は直接 `MONITORING` に戻り、180秒の検知猶予を設けます。

開始後15秒の猶予を過ぎて顔表示または十分な動きを検出した合成イベントは、入浴進行を無効化して `BATH_REQUIRED` に戻します。

## Manual Bath

ローカルUI操作で直接開始し、開始QRは使いません。完了QR合成イベントは必要です。有効時間は5分から45分で、通常はPresence Guardを適用せず、完了後は直接 `MONITORING` に戻ります。

## Riz

Rizは状態enumではなく、`intervention_source = RIZ` と `riz_active = true` の文脈です。Phone Start、Start QR、3秒連続の充電接続、通常入浴、Complete QR、10秒の接続保持を合成イベントで表します。切断またはPresence Guard違反は進行を無効化し、新しいStartイベントを要求します。画面上はオレンジで表現します。

## 例外モード

- Daily Restは合成日ごとに1回、30分です。
- Call Safe Modeは3時間内4回という過剰利用概念を示し、4回目で入浴必須になります。
- Exam Modeは検知を停止し、Riz中には開始できません。終了後は180秒の猶予があります。
- Emergency Safe Modeは技術的停止ではありません。終了時に入浴必須になります。

Technical Safety Cutoffはこの公開デモでは文書化のみです。非公開プロトタイプには実装されていますが、実Windows環境での受入れ堅牢化を継続しています。この公開版はプロセスを終了しません。
