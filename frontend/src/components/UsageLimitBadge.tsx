import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { usageApi } from '../api/usage';

export default function UsageLimitBadge() {
  const user = useAuthStore((state) => state.user);
  const [remaining, setRemaining] = useState<number | null>(null);

  useEffect(() => {
    const fetchRemaining = async () => {
      const count = await usageApi.getRemainingUsage();
      setRemaining(count);
    };

    if (user) {
      fetchRemaining();
    }
  }, [user]);

  // 管理者または未認証の場合は表示しない
  if (!user || user.role === 'admin') {
    return null;
  }

  // 残り回数が取得できない場合は表示しない
  if (remaining === null) {
    return null;
  }

  // 色を残り回数に応じて変更
  const getColor = () => {
    if (remaining === 0) return 'text-red-400 border-red-400';
    if (remaining <= 2) return 'text-orange-400 border-orange-400';
    return 'text-[var(--color-accent-secondary)] border-[var(--color-accent-secondary)]';
  };

  return (
    <div
      className={`px-3 py-1 text-xs font-mono border ${getColor()} rounded`}
      title="本日の残り使用回数"
    >
      残り {remaining}/{user.daily_limit || 5}回
    </div>
  );
}
