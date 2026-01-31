// import apiClient from './client'; // 将来のAPI実装用

// interface UsageResponse {
//   remaining: number | null; // null = 無制限
// }

export const usageApi = {
  getRemainingUsage: async (): Promise<number | null> => {
    // Note: This endpoint needs to be implemented in backend
    // For now, we'll extract from user info
    try {
      const authData = localStorage.getItem('langgraph-catalyst-auth');
      if (authData) {
        const { state } = JSON.parse(authData);
        if (state?.user?.role === 'admin') {
          return null; // 無制限
        }
        // For now, return daily_limit as remaining (backend API will be needed for accurate count)
        return state?.user?.daily_limit || 5;
      }
      return null;
    } catch (error) {
      console.error('Failed to get remaining usage:', error);
      return null;
    }
  },
};
