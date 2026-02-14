'use client';

import { useProfileStore } from '@/stores/profileStore';

export default function StepWorkIncome() {
  const { profile, updateProfile } = useProfileStore();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Work &amp; income</h2>
      <p className="mt-1 text-sm text-gray-500">Employment and income help us find relevant supports.</p>

      <div className="mt-6 space-y-5">
        {/* Employment Status */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Employment status</label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              { value: 'employed', label: '💼 Employed' },
              { value: 'self_employed', label: '🏢 Self-employed' },
              { value: 'unemployed', label: '🔍 Unemployed' },
              { value: 'retired', label: '🌴 Retired' },
              { value: 'student', label: '🎓 Student' },
              { value: 'homemaker', label: '🏠 Homemaker' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => updateProfile({ employment_status: opt.value as any })}
                className={`select-card py-3 ${profile.employment_status === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Freelancer */}
        {profile.employment_status === 'self_employed' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Are you a freelancer?</label>
            <div className="flex gap-3">
              {[true, false].map((val) => (
                <button
                  key={String(val)}
                  onClick={() => updateProfile({ is_freelancer: val })}
                  className={`select-card flex-1 py-3 ${profile.is_freelancer === val ? 'select-card-active' : ''}`}
                >
                  <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Income Bracket */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Approximate household income (gross, per year)
          </label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              { value: '<20k', label: 'Under €20k' },
              { value: '20-40k', label: '€20k - €40k' },
              { value: '40-60k', label: '€40k - €60k' },
              { value: '60-80k', label: '€60k - €80k' },
              { value: '80k+', label: 'Over €80k' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => updateProfile({ income_bracket: opt.value as any })}
                className={`select-card py-3 ${profile.income_bracket === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Work from home */}
        {(profile.employment_status === 'employed' || profile.employment_status === 'self_employed') && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Do you regularly work from home?
            </label>
            <div className="flex gap-3">
              {[true, false].map((val) => (
                <button
                  key={String(val)}
                  onClick={() => updateProfile({ works_from_home: val })}
                  className={`select-card flex-1 py-3 ${profile.works_from_home === val ? 'select-card-active' : ''}`}
                >
                  <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
