'use client';

import { useProfileStore } from '@/stores/profileStore';

export default function StepEducationBusiness() {
  const { profile, updateProfile } = useProfileStore();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Education &amp; business</h2>
      <p className="mt-1 text-sm text-gray-500">These help us find education grants and business supports.</p>

      <div className="mt-6 space-y-5">
        {/* Student / Planning education */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you currently studying or planning to study?
          </label>
          <div className="flex gap-3">
            {[
              { val: 'yes', label: 'Yes, currently' },
              { val: 'planning', label: 'Planning to' },
              { val: 'no', label: 'No' },
            ].map((opt) => (
              <button
                key={opt.val}
                onClick={() => {
                  if (opt.val === 'yes') {
                    updateProfile({ is_student: true, planning_education: false });
                  } else if (opt.val === 'planning') {
                    updateProfile({ is_student: false, planning_education: true });
                  } else {
                    updateProfile({ is_student: false, planning_education: false });
                  }
                }}
                className={`select-card flex-1 py-3 ${
                  (opt.val === 'yes' && profile.is_student) ||
                  (opt.val === 'planning' && profile.planning_education) ||
                  (opt.val === 'no' && !profile.is_student && !profile.planning_education && profile.is_student !== undefined)
                    ? 'select-card-active'
                    : ''
                }`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Business */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Do you own a business or plan to start one?
          </label>
          <div className="flex gap-3">
            {[
              { val: 'yes', label: 'Yes, I own one' },
              { val: 'planning', label: 'Planning to' },
              { val: 'no', label: 'No' },
            ].map((opt) => (
              <button
                key={opt.val}
                onClick={() => {
                  if (opt.val === 'yes') {
                    updateProfile({ owns_business: true, planning_business: false });
                  } else if (opt.val === 'planning') {
                    updateProfile({ owns_business: false, planning_business: true });
                  } else {
                    updateProfile({ owns_business: false, planning_business: false });
                  }
                }}
                className={`select-card flex-1 py-3 ${
                  (opt.val === 'yes' && profile.owns_business) ||
                  (opt.val === 'planning' && profile.planning_business) ||
                  (opt.val === 'no' && !profile.owns_business && !profile.planning_business && profile.owns_business !== undefined)
                    ? 'select-card-active'
                    : ''
                }`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Business details */}
        {(profile.owns_business || profile.planning_business) && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">How old is the business?</label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { value: 0, label: 'Not started yet' },
                  { value: 3, label: '< 6 months' },
                  { value: 12, label: '6-18 months' },
                  { value: 24, label: '> 18 months' },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => updateProfile({ business_age_months: opt.value })}
                    className={`select-card py-3 ${profile.business_age_months === opt.value ? 'select-card-active' : ''}`}
                  >
                    <span className="text-sm font-medium">{opt.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Number of employees</label>
              <input
                type="number"
                className="input"
                min={0}
                max={250}
                placeholder="0"
                value={profile.num_employees ?? ''}
                onChange={(e) => updateProfile({ num_employees: e.target.value ? Number(e.target.value) : undefined })}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
