# Anti-Sleep Turret (Ast) — Public Portfolio Edition

日中の意図しない睡眠でCG制作時間が減るという個人的な課題に対し、検知から入浴介入までを一つの状態機械として設計したN=1プロトタイプの、サニタイズ済み公開デモです。対象ユーザーは作者本人のみで、医療製品ではありません。現在のデータから因果的な有効性や効果量を示すことはできません。

開発は2026年5月31日に開始し、6月2日から実生活での個人運用を始めました。MVPの大部分は約3日で実装しましたが、その後約50日を運用試験、バグ修正、閾値調整、例外設計、安全性向上に使いました。実装前には、CLLと呼ぶ約4か月分の自己管理ログを記録・検討し、入浴後に覚醒しやすいという本人の観察をもとに、検知と入浴を接続する介入判断を採用しました。

## English executive summary

Ast is a dependency-free public simulation of a personal N=1 system that connects synthetic drowsiness signals to a timed bathing intervention. It demonstrates domain modeling, safety-oriented state transitions, exception design, deterministic scenarios, and release sanitization. It is not a medical product, and the available observations do not establish causality or effect size.

## 実行

Python 3.11以上を使用します。

```powershell
python -m pip install -e .
python -m ast_demo
```

ヘッドレスシナリオ:

```powershell
python -m ast_demo --scenario repeated-risk --headless
```

検証:

```powershell
python -m compileall .
python -m pytest -q
python scripts/verify_public_release.py
```

実センサー、カメラ処理、スマートフォン連携、ネットワーク認証、OSプロセス操作は含みません。すべての入力は合成イベントです。

詳細は [現在の実装](docs/current-implementation.md)、[公開版と非公開版の境界](docs/public-vs-private.md)、[公開マニフェスト](PUBLIC_RELEASE_MANIFEST.md) を参照してください。

## 権利

本リポジトリには現在オープンソースライセンスがありません。詳細は [NOTICE.md](NOTICE.md) を参照してください。
