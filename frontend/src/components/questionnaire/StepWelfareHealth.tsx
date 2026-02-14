'use client';

import { useProfileStore } from '@/stores/profileStore';
import { WELFARE_PAYMENT_OPTIONS } from '@/types';

export default function StepWelfareHealth() {
  const { profile, updateProfile } = useProfileStore();
  const payments = profile.welfare_payments || [];

  const togglePayment = (value: string) => {
    const current = [...payments];
    const idx = current.indexOf(value);
    if (idx >= 0) {
      current.splice(idx, 1);
    } else {
      current.push(value);
    }
    updateProfile({ welfare_payments: current });
  };

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Welfare &amp; health</h2>
      <p className="mt-1 text-sm text-gray-500">Welfare payments and health info unlock additional supports.</p>

      <div className="mt-6 space-y-5">
        {/* Welfare Payments */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you receiving any of these welfare payments? (select all that apply)
          </label>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {WELFARE_PAYMENT_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => togglePayment(opt.value)}
                className={`flex items-center gap-3 rounded-lg border-2 px-4 py-3 text-left transition-all ${
                  payments.includes(opt.value)
                    ? 'border-brand-500 bg-brand-50'
                    : 'border-gray-200 hover:border-brand-300'
                }`}
              >
                <span className={`flex h-5 w-5 items-center justify-center rounded border-2 ${
                  payments.includes(opt.value)
                    ? 'border-brand-500 bg-brand-500 text-white'
                    : 'border-gray-300'
                }`}>
                  {payments.includes(opt.value) && (
                    <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </span>
                <span className="text-sm font-medium text-gray-700">{opt.label}</span>
              </button>
            ))}
            <button
              onClick={() => updateProfile({ welfare_payments: [] })}
              className={`flex items-center gap-3 rounded-lg border-2 px-4 py-3 text-left transition-all ${
                payments.length === 0
                  ? 'border-brand-500 bg-brand-50'
                  : 'border-gray-200 hover:border-brand-300'
              }`}
            >
              <span className="text-sm font-medium text-gray-700">None of the above</span>
            </button>
          </div>
        </div>

        {/* Medical Card */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Do you have a Medical Card?</label>
          <div className="flex gap-3">
            {[
              { value: true, label: 'Yes' },
              { value: false, label: 'No' },
            ].map((opt) => (
              <button
                key={String(opt.value)}
                onClick={() => updateProfile({ has_medical_card: opt.value })}
                className={`select-card flex-1 py-3 ${profile.has_medical_card === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Disability */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Does anyone in your household have a disability?
          </label>
          <div className="flex gap-3">
            {[
              { val: 'self', label: 'Yes, me' },
              { val: 'household', label: 'Yes, someone else' },
              { val: 'no', label: 'No' },
            ].map((opt) => (
              <button
                key={opt.val}
                onClick={() => {
                  if (opt.val === 'self') {
                    updateProfile({ has_disability: true, household_disability: false });
                  } else if (opt.val === 'household') {
                    updateProfile({ has_disability: false, household_disability: true });
                  } else {
                    updateProfile({ has_disability: false, household_disability: false });
                  }
                }}
                className={`select-card flex-1 py-3 ${
                  (opt.val === 'self' && profile.has_disability) ||
                  (opt.val === 'household' && profile.household_disability) ||
                  (opt.val === 'no' && !profile.has_disability && !profile.household_disability && profile.has_disability !== undefined)
                    ? 'select-card-active'
                    : ''
                }`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Medical expenses */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Have you paid for any medical expenses this year?
          </label>
          <p className="text-xs text-gray-400 mb-2">GP visits, prescriptions, dental, hospital, physio, etc. — even if partly covered by insurance, you can claim 20% tax relief on the amount you paid out of pocket</p>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ has_medical_expenses: val })}
                className={`select-card flex-1 py-3 ${profile.has_medical_expenses === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Visual Impairment */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you or your spouse blind or severely visually impaired?
          </label>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ is_visually_impaired: val })}
                className={`select-card flex-1 py-3 ${profile.is_visually_impaired === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Nursing Home Expenses */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you paying nursing home fees for yourself or a family member?
          </label>
          <p className="text-xs text-gray-400 mb-2">You can claim tax relief at your highest rate on nursing home fees</p>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ has_nursing_home_expenses: val })}
                className={`select-card flex-1 py-3 ${profile.has_nursing_home_expenses === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
