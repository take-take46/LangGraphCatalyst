import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright E2E Test Configuration
 *
 * ドキュメント: https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  // テストディレクトリ
  testDir: './e2e',

  // 並列実行の設定
  fullyParallel: true,

  // CI環境でのリトライ設定
  retries: process.env.CI ? 2 : 0,

  // ワーカー数（並列実行数）
  workers: process.env.CI ? 1 : undefined,

  // レポーター設定
  reporter: process.env.CI
    ? [
        ['html'],
        ['github'],
        ['junit', { outputFile: 'playwright-report/results.xml' }],
      ]
    : [['html'], ['list']],

  // 共通設定
  use: {
    // ベースURL（環境変数で上書き可能）
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173',

    // スクリーンショット設定
    screenshot: 'only-on-failure',

    // ビデオ録画設定
    video: 'retain-on-failure',

    // トレース設定（デバッグ用）
    trace: 'on-first-retry',

    // タイムアウト設定
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  // グローバルタイムアウト
  timeout: 60000,

  // テストプロジェクト（CI/CDではChromiumのみ、ローカルでは全ブラウザ）
  projects: process.env.CI
    ? [
        // CI環境: Chromiumのみ（高速化）
        {
          name: 'chromium',
          use: { ...devices['Desktop Chrome'] },
        },
      ]
    : [
        // ローカル環境: 全ブラウザ
        {
          name: 'chromium',
          use: { ...devices['Desktop Chrome'] },
        },
        {
          name: 'firefox',
          use: { ...devices['Desktop Firefox'] },
        },
        {
          name: 'webkit',
          use: { ...devices['Desktop Safari'] },
        },
        {
          name: 'Mobile Chrome',
          use: { ...devices['Pixel 5'] },
        },
        {
          name: 'Mobile Safari',
          use: { ...devices['iPhone 12'] },
        },
      ],

  // 開発サーバー設定（ローカル実行時）
  webServer: process.env.CI
    ? undefined
    : {
        command: 'npm run dev',
        url: 'http://localhost:5173',
        reuseExistingServer: !process.env.CI,
        timeout: 120000,
      },
});
