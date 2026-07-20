# 開発履歴

## 全体像

- 開発開始: 2026-05-31
- 実運用開始: 2026-06-02
- MVP: 約3日
- 改善期間: 2026-07-20時点で約50日

個別フェーズの日付は記録から確定できないため、ここでは正確な日付を割り当てず、判断の順序として示します。

| Phase | 主題 | 人間が行った中心判断 |
| ---: | --- | --- |
| 1 | CLL bottleneck discovery | 約4か月のCLLから、CG制作時間を失わせる日中の寝落ちを対象に選んだ |
| 2 | Graded warnings | 即時強制だけでなくLv1・Lv2の段階を設けた |
| 3 | Bath intervention | 通常アラームではなく入浴を中心介入にした |
| 4 | Return / Recovery experiment and retirement | 試行後、現行標準フローから外した |
| 5 | Exception modes | 正当な利用中断を明示的な状態として扱った |
| 6 | Risk repetition and Presence Guard | 単発閾値以外の反復と、入浴開始後の在席を扱った |
| 7 | Riz continuity | スマートフォン起点の文脈を同じBath状態機械に統合した |
| 8 | Runtime safety and Technical Safety Cutoff | 強制より安全を優先し、外部の技術的停止境界を選んだ |

各フェーズの「観察された問題 / Human decision / Codex-assisted implementation / Validation / Remaining limitation」は [反復履歴](iteration-history.md) に記録します。
