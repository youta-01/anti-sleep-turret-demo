# 反復履歴

個別フェーズの正確な日付は既知ではありません。開発は2026-05-31に始まり、2026-06-02に実運用を開始しました。MVPは約3日、その後2026-07-20時点まで約50日改善しています。

## 1. CLL problem selection

- **Observed context:** 約4か月のCLLを振り返り、CG制作中の日中の寝落ちを個人用システムの設計対象として選んだ。
- **Human decision:** 作者本人を対象に、検知から介入までを扱う問題として定義した。
- **Codex-assisted implementation:** 観察を実装可能な入力、状態、イベントの骨組みに落とした。
- **Validation:** CLLの振り返りと本人の実運用目的が一致するかを確認した。
- **Remaining limitation:** 後ろ向きのN=1観察であり、原因や一般性を示さない。

## 2. Graded warnings

- **Observed problem:** 即時の強制介入だけでは、軽い兆候と強い兆候を区別できない。
- **Human decision:** MONITORINGからLv1、Lv2、Bathへ段階的に介入する方針を選んだ。
- **Codex-assisted implementation:** 閾値計算、警告状態、決定的シナリオ、回帰テストを実装した。
- **Validation:** 合成入力で各閾値と信号解消時の遷移を検証した。
- **Remaining limitation:** 公開デモの値は仕様説明用で、科学的な検出精度を示さない。

## 3. Bath intervention

- **Design gap:** アラームだけでは、入浴という介入の開始と完了を状態として扱えない。
- **Human decision:** 入浴を中心介入にし、開始と完了を明示的に扱うことを選んだ。
- **Codex-assisted implementation:** BATH_REQUIRED、BATH_STARTED、BATH_TIMEOUTと時間ポリシーを実装した。
- **Validation:** 早すぎる完了、正常完了、タイムアウトをFake Clockでテストした。
- **Remaining limitation:** 公開版は合成イベントの遷移検証であり、行動上の効果を測定しない。

## 4. Return / Recovery experiment and retirement

- **Observed change:** 以前の版では、Bath後にReturn to PCとRecovery Workを経由するフローを試した。
- **Human decision:** 実運用後、Return to PCとRecovery Workを現行の標準フローから外した。
- **Codex-assisted implementation:** 公開状態enumとUIから除外し、Bath完了後をMONITORINGへ直結した。
- **Validation:** 廃止状態が公開モデルに存在しないことをテストした。
- **Evidence boundary:** 廃止理由は公開資料から確定できる範囲を越えて説明しない。非公開プロトタイプには休眠中の互換コードが残る。

## 5. Exception modes

- **Observed problem:** 強制だけでは通話、試験、休憩、障害対応など正当な事情を扱えない。
- **Human decision:** 回避用の曖昧な抜け道ではなく、条件付きの明示的例外を設けた。
- **Codex-assisted implementation:** Daily Rest、Call Safe Mode、Exam Mode、Emergency Safe Modeを状態機械へ追加した。
- **Validation:** 回数制限、終了遷移、猶予、Rizとの競合をテストした。
- **Remaining limitation:** あらゆる現実の例外を網羅できるわけではなく、ポリシーの継続調整が必要。

## 6. Risk repetition and Presence Guard

- **Observed problem:** 単発閾値だけでは反復する中程度リスクを扱えず、Bath開始後の在席も検出したかった。
- **Human decision:** Risk 50を60分内に3回、Risk 35以下15秒で再アームする方針とPresence Guardを選んだ。
- **Codex-assisted implementation:** Repetition Guard、再アーム、時間窓、Presence違反時の無効化を実装した。
- **Validation:** 重複カウント防止、時間窓、3回目の強制、Presence猶予をテストした。
- **Remaining limitation:** 閾値は作者向け運用ポリシーで、一般的な最適値ではない。

## 7. Riz continuity

- **Observed problem:** スマートフォン起点の介入を別状態にすると、Bathロジックが重複しやすい。
- **Human decision:** Rizを独立状態ではなく、同じBath状態機械の介入元と表示文脈にした。
- **Codex-assisted implementation:** Start QR、充電安定、切断無効化、完了保持、オレンジ表示を統合した。
- **Validation:** 開始から完了までの連続性、途中切断、Presence違反をテストした。
- **Remaining limitation:** 公開版は合成イベントのみで、実スマートフォン通信は含まない。

## 8. Runtime safety and Technical Safety Cutoff

- **Observed problem:** 回避耐性を高めるほど停止コストが増え、アプリ不具合が一般のPC利用を妨げる危険が生じた。
- **Human decision:** 強制より安全を上位に置き、アプリ外のTechnical Safety Cutoffを設ける方針を選んだ。
- **Codex-assisted implementation:** 安全境界の文書化、公開境界、Windows側の受け入れ確認項目を整備した。
- **Validation:** 公開デモでは安全設計と回帰テストを確認した。
- **Remaining limitation:** Technical Safety Cutoffが完全に検証済みとは言えず、実Windowsでの受け入れ強化は継続中。
