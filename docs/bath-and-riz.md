# BathとRiz

## 強制Bath

`BATH_REQUIRED` で有効なStart QRを受けると `BATH_STARTED` に進みます。公開モデルの強制Bathは8分以上15分以内で完了できます。早すぎる完了は受理せず、最大時間を超えると `BATH_TIMEOUT` になります。正常完了後は直接 `MONITORING` に戻り、180秒の検知猶予を設けます。

開始15秒後からPresence Guardが有効です。顔または十分な動きを検出した場合、開始情報を無効化し、新しいStartイベントが必要な `BATH_REQUIRED` に戻します。

## Manual Bath

Manual Bathは `MONITORING` から本人が開始します。Start QRとPresence Guardを要求せず、5〜45分の範囲で完了できます。これは自発的な入浴を、強制フローとは異なる方針で同じ状態機械に載せるものです。

If Manual Bath exceeds 45 minutes, it returns directly to `MONITORING` and records `manual bath timed out`. It cannot be restarted with Start QR; the user must invoke Manual Bath again. Forced Bath and Riz instead remain in `BATH_TIMEOUT` and require a new Start QR.

## Riz

Rizは新しい状態enumではなく、`intervention_source = RIZ` と表示文脈の組み合わせです。スマートフォン起点で `BATH_REQUIRED` を開始し、画面はオレンジ色になります。

Rizでは、Start QRに加えて充電接続が3秒安定すると `BATH_STARTED` へ進みます。途中の切断やPresence Guard違反は開始を無効化します。完了QR後も充電接続を10秒保持してから `MONITORING` に戻ります。

## 例外モード

- Daily Rest: 1日1回、30分。
- Call Safe Mode: 3時間内の利用回数を数え、4回目はBathを要求。
- Exam Mode: 検知を止める。Riz中は開始不可。終了後180秒の猶予。
- Emergency Safe Mode: 技術的な外部停止ではない。終了時にBathを要求。

Technical Safety Cutoffはこれらの状態とは別で、State Machineの外側に置きます。現在の実Windows環境での受け入れ強化は継続中です。
