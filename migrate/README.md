# GUI関連ファイル移行フォルダ

このフォルダには、Qt-Theme-Managerライブラリから分離されたGUI関連ファイルが含まれています。これらのファイルは、将来的にqt-theme-studioリポジトリに手動で移行される予定です。

## 移行済みファイル一覧

### GUI起動スクリプト
- `launch_theme_editor.py` - テーマエディター起動スクリプト
- `launch_zebra_theme_editor.py` - ゼブラパターンエディター起動スクリプト
- `launch_gui_preview.py` - GUIプレビュー起動スクリプト

### エディタ関連ファイル
- `theme_editor_zebra_extension.py` - テーマエディター拡張機能
- `zebra_pattern_editor.py` - ゼブラパターンエディター本体
- `analyze_zebra_colors.py` - ゼブラ色分析ツール
- `improve_zebra_colors.py` - ゼブラ色改善ツール

### ディレクトリ
- `examples/` - サンプルコードとデモ
- `scripts/` - ユーティリティスクリプト
- `utils/` - ヘルパーモジュール

## 移行プロセス

### 1. 自動移行（完了済み）
- すべての対象ファイルが元の場所から`migrate/`フォルダに移動
- 元のディレクトリ構造が保持
- ファイルの整合性が確認済み

### 2. 手動移行（今後の作業）
以下の作業は人間が手動で実行する必要があります：

1. **qt-theme-studioリポジトリへの移行**
   - `migrate/`フォルダの内容をqt-theme-studioリポジトリに移行
   - 必要に応じてファイル構造の調整
   - 動作確認とテスト

2. **移行完了後のクリーンアップ**
   - qt-theme-studioでの動作確認完了後
   - `migrate/`フォルダの削除
   - ドキュメント内の古い参照の更新

## 検証ツール

### migration_status.md
移行状況の概要と次のステップを記載

### verify_migration.py
移行の完全性を検証するスクリプト
```bash
python migrate/verify_migration.py
```

### migration_verification_report.txt
検証結果の詳細レポート（自動生成）

## 注意事項

- **削除禁止**: AIは`migrate/`フォルダの削除を行いません
- **手動作業**: qt-theme-studioへの実際の移行は人間が実行
- **構造保持**: 移行時は元のディレクトリ構造を維持
- **動作確認**: 移行後は必ず動作確認を実施

## 移行後の影響

### ライブラリ側（qt-theme-manager）
- コアライブラリ機能のみに集中
- パッケージサイズの削減
- 依存関係の最小化
- 保守性の向上

### GUI側（qt-theme-studio）
- GUI機能の独立した開発
- 専用の機能拡張
- ユーザビリティの向上
- 独立したリリースサイクル

## 関連ドキュメント

- `.kiro/specs/library-separation/requirements.md` - 要件定義
- `.kiro/specs/library-separation/design.md` - 設計仕様
- `.kiro/specs/library-separation/tasks.md` - 実装計画