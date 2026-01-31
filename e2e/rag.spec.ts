import { test, expect } from '@playwright/test';

test.describe('RAG学習支援フロー', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('ホームページからRAGページに遷移できる', async ({ page }) => {
    await page.click('text=RAG学習支援');
    await expect(page).toHaveURL(/.*rag/);
    await expect(page.locator('h1')).toContainText('RAG学習支援');
  });

  test('サンプル質問をクリックして入力フィールドに反映される', async ({ page }) => {
    await page.goto('/rag');

    // サンプル質問をクリック
    await page.click('text=LangGraphでステートグラフを作成');

    // 入力フィールドに質問が反映されているか確認
    const input = page.locator('textarea[placeholder*="LangGraphについて質問"]');
    await expect(input).toHaveValue(/LangGraphでステートグラフ/);
  });

  test('質問を送信して回答を受け取る', async ({ page }) => {
    await page.goto('/rag');

    // 質問を入力
    const input = page.locator('textarea[placeholder*="LangGraphについて質問"]');
    await input.fill('LangGraphとは何ですか？');

    // 送信ボタンをクリック
    await page.click('button:has-text("送信")');

    // ローディング状態を確認
    await expect(page.locator('text=回答を生成中')).toBeVisible({ timeout: 1000 });

    // 回答が表示されるまで待機
    await expect(page.locator('text=LangGraphとは何ですか？')).toBeVisible({ timeout: 10000 });

    // アシスタントの回答が表示されることを確認
    // NOTE: MSWモックが動作していれば、モックレスポンスが返される
    await expect(page.locator('.assistant-message')).toBeVisible({ timeout: 15000 });
  });

  test('ソース情報が表示される', async ({ page }) => {
    await page.goto('/rag');

    const input = page.locator('textarea[placeholder*="LangGraphについて質問"]');
    await input.fill('テスト質問');
    await page.click('button:has-text("送信")');

    // ソースセクションが表示されるまで待機
    await expect(page.locator('text=参照ソース').or(page.locator('text=ソース'))).toBeVisible({ timeout: 15000 });
  });

  test('コード例が表示される', async ({ page }) => {
    await page.goto('/rag');

    const input = page.locator('textarea[placeholder*="LangGraphについて質問"]');
    await input.fill('コード例を見せてください');
    await page.click('button:has-text("送信")');

    // コードブロックが表示されるまで待機
    await expect(page.locator('pre code')).toBeVisible({ timeout: 15000 });
  });

  test('空の質問は送信できない', async ({ page }) => {
    await page.goto('/rag');

    // 送信ボタンをクリック（入力なし）
    await page.click('button:has-text("送信")');

    // ローディング状態にならないことを確認
    await expect(page.locator('text=回答を生成中')).not.toBeVisible({ timeout: 1000 });
  });
});
