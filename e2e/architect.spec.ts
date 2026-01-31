import { test, expect } from '@playwright/test';

test.describe('構成案生成フロー', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('ホームページから構成案生成ページに遷移できる', async ({ page }) => {
    await page.click('text=構成案生成');
    await expect(page).toHaveURL(/.*architect/);
    await expect(page.locator('h1')).toContainText('構成案生成');
  });

  test('サンプル課題をクリックして入力フィールドに反映される', async ({ page }) => {
    await page.goto('/architect');

    // サンプル課題をクリック
    await page.click('text=カスタマーサポート');

    // 入力フィールドに課題が反映されているか確認
    const textarea = page.locator('textarea[placeholder*="ビジネス課題"]');
    await expect(textarea).toHaveValue(/カスタマーサポート/);
  });

  test('ビジネス課題を入力して構成案を生成できる', async ({ page }) => {
    await page.goto('/architect');

    // ビジネス課題を入力
    const challengeInput = page.locator('textarea[placeholder*="ビジネス課題"]');
    await challengeInput.fill('データ分析ワークフローを自動化したい');

    // 業界を入力（オプション）
    const industryInput = page.locator('input[placeholder*="例: EC"]');
    await industryInput.fill('製造業');

    // 構成案生成ボタンをクリック
    await page.click('button:has-text("構成案を生成")');

    // ローディング状態を確認
    await expect(page.locator('text=構成案を生成中')).toBeVisible({ timeout: 1000 });

    // 結果が表示されるまで待機
    await expect(page.locator('text=課題分析').or(page.locator('text=分析結果'))).toBeVisible({ timeout: 15000 });
  });

  test('Mermaid図が表示される', async ({ page }) => {
    await page.goto('/architect');

    const challengeInput = page.locator('textarea[placeholder*="ビジネス課題"]');
    await challengeInput.fill('テスト課題');
    await page.click('button:has-text("構成案を生成")');

    // Mermaid図が表示されるまで待機
    // NOTE: MermaidDiagramコンポーネントがレンダリングするSVGまたはDIVを確認
    await expect(page.locator('.mermaid').or(page.locator('text=アーキテクチャ図'))).toBeVisible({ timeout: 15000 });
  });

  test('コード例が表示される', async ({ page }) => {
    await page.goto('/architect');

    const challengeInput = page.locator('textarea[placeholder*="ビジネス課題"]');
    await challengeInput.fill('テスト課題');
    await page.click('button:has-text("構成案を生成")');

    // コードブロックが表示されるまで待機
    await expect(page.locator('pre code')).toBeVisible({ timeout: 15000 });
  });

  test('ビジネス向け説明が表示される', async ({ page }) => {
    await page.goto('/architect');

    const challengeInput = page.locator('textarea[placeholder*="ビジネス課題"]');
    await challengeInput.fill('テスト課題');
    await page.click('button:has-text("構成案を生成")');

    // ビジネス説明セクションが表示されるまで待機
    await expect(page.locator('text=ビジネス向け説明').or(page.locator('text=わかりやすい説明'))).toBeVisible({ timeout: 15000 });
  });

  test('空の課題は送信できない', async ({ page }) => {
    await page.goto('/architect');

    // 送信ボタンをクリック（入力なし）
    await page.click('button:has-text("構成案を生成")');

    // ローディング状態にならないことを確認
    await expect(page.locator('text=構成案を生成中')).not.toBeVisible({ timeout: 1000 });
  });

  test('制約条件を追加できる', async ({ page }) => {
    await page.goto('/architect');

    const challengeInput = page.locator('textarea[placeholder*="ビジネス課題"]');
    await challengeInput.fill('テスト課題');

    // 制約条件を入力
    const constraintsInput = page.locator('input[placeholder*="各制約条件を入力"]');
    await constraintsInput.fill('日本語対応必須');
    await constraintsInput.press('Enter');

    // 制約条件が追加されたことを確認
    await expect(page.locator('text=日本語対応必須')).toBeVisible();
  });
});
