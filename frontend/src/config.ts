// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

// Other configuration variables can be added here
export const config = {
    apiUrl: API_URL,
    defaultLocale: 'en-IN',
    currency: 'INR',
    dateFormat: {
        short: {
            day: 'numeric' as const,
            month: 'short' as const,
            year: 'numeric' as const
        }
    }
}; 