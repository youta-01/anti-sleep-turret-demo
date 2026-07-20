# Public Release Manifest

## 公開対象

- `src/ast_demo/`: 依存なしのドメインロジック、CLI、Tkinter UI
- `tests/`: リスク、episode、Bath、Riz、例外、公開境界のテスト
- `scripts/verify_public_release.py`: 追跡候補ファイルの安全検査
- `docs/`: 現行仕様、設計判断、開発経緯、サニタイズ済みメディア
- `.github/workflows/ci.yml`: Python 3.11のLinux / Windows検証
- ルート文書とパッケージ設定

## 明示的な除外

ローカル設定、秘密情報、実行時記録、個人データ、受信メディア、非公開実装コードは公開対象外です。公開デモは合成イベントのみを扱い、ドメイン遷移中にファイルを書きません。

公開先は `youta-01/anti-sleep-turret-demo` です。全公開チェックの合格後に `main` のみを公開します。
