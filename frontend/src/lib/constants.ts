export const APP_NAME = 'GrantFinder Ireland';
export const APP_DESCRIPTION = 'Discover every government grant, scheme, and entitlement you qualify for in Ireland.';
export const APP_URL = 'https://grantfinder.ie';

export const PRICING = {
  report: {
    name: 'Single Report',
    price: '€4.99',
    priceId: 'price_report_single',
    features: [
      'Full eligibility explanation for all grants',
      'Step-by-step application guides',
      'Required documents checklist',
      'Downloadable PDF report',
    ],
  },
  monthly: {
    name: 'Premium Monthly',
    price: '€2.99/mo',
    priceId: 'price_premium_monthly',
    features: [
      'Everything in Single Report',
      'Unlimited scans & reports',
      'Grant alerts & notifications',
      'AI chat advisor',
      'Deadline reminders',
    ],
  },
  annual: {
    name: 'Premium Annual',
    price: '€24.99/yr',
    priceId: 'price_premium_annual',
    savings: 'Save €10.89',
    features: [
      'Everything in Premium Monthly',
      'Best value — 2 months free',
    ],
  },
};
