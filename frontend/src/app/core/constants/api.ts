export const API = {
  BASE_URL: typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://ai-insurance-portal.onrender.com',
  API_V1: '/api/v1',

  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    PROFILE: '/users/me',
  },

  USERS: '/users',


  UPLOAD: {
    IMAGE: '/upload/image',
    DOCUMENT: '/upload/document',
  },

  AI: {
    ANALYZE: '/ai/analyze',
    REPORT: '/ai/report',
    MY_REPORTS: '/ai/reports/my',
    ALL_REPORTS: '/ai/reports',
  },


  DASHBOARD: {
    SUMMARY: '/dashboard/summary',
  },

  CLAIMS: {
    LIST: '/claims/',
    MY: '/claims/my',
    DETAILS: '/claims',
    CREATE: '/claims/',
    UPDATE: '/claims',
    DELETE: '/claims',
  },

  POLICIES: {
    LIST: '/policies/',
    MY: '/policies/my',
    DETAILS: '/policies',
    CREATE: '/policies/',
    UPDATE: '/policies',
    DELETE: '/policies',
  },

  PLANS: {
    LIST: '/plans/',
    DETAILS: '/plans',
    CREATE: '/plans/',
    UPDATE: '/plans',
    DELETE: '/plans',
  },
  NOTIFICATIONS: {
    LIST: '/notifications/',
    UNREAD_COUNT: '/notifications/unread-count',
    READ: '/notifications',
    READ_ALL: '/notifications/read-all',
  },

};
