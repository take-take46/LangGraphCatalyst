import { test, expect } from '@playwright/test';

/**
 * Smoke Tests - API使用料が一切かからないテスト
 *
 * このテストでは以下のみを検証:
 * - ページの表示
 * - ナビゲーション
 * - 認証フロー（ログイン/ログアウト）
 * - UIコンポーネントの表示
 *
 * ❌ テストしないもの（手動テストで確認）:
 * - RAG機能（OpenAI API使用）
 * - 構成案生成機能（OpenAI API使用）
 */

test.describe('Smoke Tests - No API Calls', () => {
  test('should display homepage @smoke', async ({ page }) => {
    await page.goto('/');

    // ページタイトル確認
    await expect(page).toHaveTitle(/LangGraph Catalyst/);

    // ヘッダーが表示される
    await expect(page.locator('header')).toBeVisible();

    // ナビゲーションリンクが表示される
    await expect(page.locator('a[href="/"]')).toBeVisible();
  });

  test('should navigate to all pages @smoke', async ({ page }) => {
    await page.goto('/');

    // ホームページ
    await expect(page).toHaveURL('/');

    // 学習パスページ（認証不要）
    await page.goto('/learning-path');
    await expect(page).toHaveURL('/learning-path');
    await expect(page.locator('h1:has-text("学習パス")')).toBeVisible();

    // テンプレートページ（認証不要）
    await page.goto('/templates');
    await expect(page).toHaveURL('/templates');
    await expect(page.locator('h1:has-text("テンプレート")')).toBeVisible();
  });

  test('should redirect to login when accessing protected pages @smoke', async ({ page }) => {
    // RAGページにアクセス（保護されている）
    await page.goto('/rag');

    // ログインページにリダイレクト
    await expect(page).toHaveURL(/.*login/);
    await expect(page.locator('input[id="username"]')).toBeVisible();

    // 構成案生成ページにアクセス（保護されている）
    await page.goto('/architect');

    // ログインページにリダイレクト
    await expect(page).toHaveURL(/.*login/);
  });

  test('should display login form @smoke', async ({ page }) => {
    await page.goto('/login');

    // ログインフォームが表示される
    await expect(page.locator('input[id="username"]')).toBeVisible();
    await expect(page.locator('input[id="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should show validation error for empty login @smoke', async ({ page }) => {
    await page.goto('/login');

    // 空のまま送信
    await page.click('button[type="submit"]');

    // HTML5バリデーションまたはカスタムバリデーションが動作
    // (ブラウザによって挙動が異なるため、ページ遷移しないことのみ確認)
    await expect(page).toHaveURL(/.*login/);
  });

  test('should display learning path topics @smoke', async ({ page }) => {
    await page.goto('/learning-path');

    // レベル選択タブが表示される
    await expect(page.locator('button:has-text("初級"), button:has-text("中級"), button:has-text("上級")')).toBeVisible();

    // トピックカードが表示される（少なくとも1つ）
    const topicCards = page.locator('[class*="card"], [class*="Card"]');
    await expect(topicCards.first()).toBeVisible();
  });

  test('should display templates with filtering @smoke', async ({ page }) => {
    await page.goto('/templates');

    // カテゴリフィルタが表示される
    await expect(page.locator('select, button:has-text("カテゴリ")')).toBeVisible();

    // テンプレートカードが表示される（少なくとも1つ）
    const templateCards = page.locator('[class*="card"], [class*="Card"]');
    await expect(templateCards.first()).toBeVisible();
  });

  test('should have responsive header @smoke', async ({ page }) => {
    await page.goto('/');

    // モバイルサイズに変更
    await page.setViewportSize({ width: 375, height: 667 });

    // ヘッダーが表示される
    await expect(page.locator('header')).toBeVisible();

    // デスクトップサイズに変更
    await page.setViewportSize({ width: 1920, height: 1080 });

    // ヘッダーが表示される
    await expect(page.locator('header')).toBeVisible();
  });

  test('should display 404 for invalid routes @smoke', async ({ page }) => {
    await page.goto('/invalid-route-12345');

    // ホームページにリダイレクトまたは404ページ表示
    // (App.tsxの設定により、"*" は "/" にリダイレクト)
    await expect(page).toHaveURL('/');
  });
});

test.describe('Authentication Flow - No API Calls', () => {
  test('should show error with invalid credentials @smoke', async ({ page }) => {
    await page.goto('/login');

    // 無効な認証情報（存在しないユーザー）
    await page.fill('input[name="username"]', 'nonexistent-user-12345');
    await page.fill('input[name="password"]', 'wrong-password-12345');

    await page.click('button[type="submit"]');

    // エラーメッセージが表示される（APIエラーまたはバリデーションエラー）
    // 認証失敗のエラーメッセージを待機（最大5秒）
    const errorMessage = page.locator('text=/認証に失敗|Invalid|Error|エラー/i');
    await expect(errorMessage).toBeVisible({ timeout: 5000 });
  });

  test('should persist login state in localStorage @smoke', async ({ page }) => {
    await page.goto('/login');

    // localStorageをチェック（ログイン前は空）
    const authStateBefore = await page.evaluate(() => localStorage.getItem('auth-storage'));
    expect(authStateBefore).toBeTruthy(); // Zustand persistによりキーは存在

    // 注: 実際のログインはAPIを使用するため、ここではlocalStorageの存在のみ確認
  });
});

test.describe('Accessibility Checks', () => {
  test('should have accessible navigation @smoke', async ({ page }) => {
    await page.goto('/');

    // キーボードナビゲーション（Tab）が機能する
    await page.keyboard.press('Tab');

    // フォーカスが移動したことを確認
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT']).toContain(focusedElement);
  });

  test('should have alt text for images @smoke', async ({ page }) => {
    await page.goto('/');

    // 画像がある場合、alt属性が設定されているか確認
    const images = await page.locator('img').all();

    for (const img of images) {
      const alt = await img.getAttribute('alt');
      // alt属性は必須（空文字列でも可）
      expect(alt).not.toBeNull();
    }
  });
});
