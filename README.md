# Anti-Sleep Turret (Ast)

CG制作・作業時間を阻害していた日中の寝落ちに対し、眠気リスク検知から入浴介入までを状態遷移として設計した個人用Windowsプロトタイプ。

![Ast production prototype demonstration](docs/images/production-demo.gif)

> Production prototype UI demonstration showing Monitoring, rising risk, Lv2 Warning, and Bath Started. This is not a scientific accuracy demonstration.

## 3つの設計ポイント

- **段階的介入** — 合成入力から Sleep Risk を算出し、Lv1・Lv2の警告を経て入浴要求へ遷移します。
- **回避耐性と継続利用の両立** — Risk 50の反復、Presence Guard、明示的な例外モードを、ひとつの状態機械で扱います。
- **安全を強制より上位に置く** — アプリ内制御とは独立した Technical Safety Cutoff を設計上の外側に置きます。実Windows環境での受け入れ強化は継続中です。

## Quick Start

Python 3.11以上を使用します。

```powershell
python -m pip install -e .
python -m ast_demo
```

ヘッドレスで決定的シナリオを実行する場合:

```powershell
python -m ast_demo --scenario repeated-risk --headless
```

[![CI](https://github.com/youta-01/anti-sleep-turret-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/youta-01/anti-sleep-turret-demo/actions/workflows/ci.yml)
![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

## English executive summary

Ast is a sanitized, dependency-free public simulation of an N=1 personal system that connects synthetic drowsiness signals to a timed bathing intervention. It demonstrates domain modeling, safety-oriented state transitions, exception policies, deterministic scenarios, and release sanitization. It is not a medical product, and current observations do not establish causality, effect size, or general reliability.

## 画面

| 状態 | 画面と説明 |
| --- | --- |
| Monitoring | ![Monitoring](docs/images/monitoring.png)<br>通常監視UI。現在の Sleep Risk と Risk 50 episode count を表示。 |
| Lv2 Warning | ![Lv2 Warning](docs/images/lv2-risk-episodes.png)<br>Risk 50に到達し、2回のepisodeを記録。次の有効なepisodeで Bath Requiredを強制する状態。 |
| Bath Required | ![Bath Required](docs/images/bath-required.png)<br>Emergency Safe Mode終了後、システムが入浴介入を要求した状態。 |
| Riz | ![Riz mode](docs/images/riz-mode.png)<br>同じBath状態機械を使い、オレンジ色のモード文脈で表示する、スマートフォン起点のRiz。 |

動画版: [production-demo.mp4](docs/images/production-demo.mp4)

## この公開版について

公開版は、実機センサーや個人データを含まないポートフォリオ用デモです。すべての入力は合成イベントで、ドメイン遷移の途中にファイルを書きません。実カメラ処理、スマートフォン連携、認証情報、ローカル設定、実行時ログ、Windowsプロセス制御は含みません。

- [問題と対象ユーザー](docs/problem-and-user.md)
- [現在のアーキテクチャ](docs/architecture.md)
- [状態遷移](docs/state-transitions.md)
- [BathとRiz](docs/bath-and-riz.md)
- [開発履歴](docs/development-history.md) / [反復履歴](docs/iteration-history.md)
- [実運用上の観察と限界](docs/evidence-and-limitations.md)
- [Human / ChatGPT / Codexの責任分担](docs/ai-collaboration.md)
- [設計判断](docs/decisions/001-bathing-over-alarm-only.md)
- [エントリーシート素材](docs/entry-sheet-summary.md)
- [公開版と非公開版の境界](docs/public-vs-private.md)
- [公開マニフェスト](PUBLIC_RELEASE_MANIFEST.md)

## 検証

```powershell
python -m compileall .
python -m pytest -q
python scripts/verify_public_release.py
```

## 注意

対象ユーザーは作者本人です。運転、産業監視、医療上の診断・治療、他者の制御を目的としません。現在の記録から、医学的有効性、因果効果、効果量、一般利用者への有効性を主張することはできません。

## 権利

現時点ではオープンソースライセンスを付与していません。詳細は [NOTICE.md](NOTICE.md) を参照してください。
