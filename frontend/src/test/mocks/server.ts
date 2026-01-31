import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// テスト用のMSWサーバーをセットアップ
export const server = setupServer(...handlers);
