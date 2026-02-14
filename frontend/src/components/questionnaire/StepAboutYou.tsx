'use client';

import { useProfileStore } from '@/stores/profileStore';
import { IRISH_COUNTIES } from '@/types';

export default function StepAboutYou() {
  const { profile, updateProfile } = useProfileStore();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Let&apos;s start with you</h2>
      <p className="mt-1 text-sm text-gray-500">Basic info to help us match you with the right grants.</p>

      <div className="mt-6 space-y-5">
        {/* Age */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Your age</label>
          <input
            type="number"
            className="input"
            placeholder="e.g. 35"
            min={16}
            max={120}
            value={profile.age || ''}
            onChange={(e) => updateProfile({ age: e.target.value ? Number(e.target.value) : undefined })}
          />
        </div>

        {/* County */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">County</label>
          <select
            className="input"
            value={profile.county || ''}
            onChange={(e) => updateProfile({ county: e.target.value || undefined })}
          >
            <option value="">Select your county</option>
            {IRISH_COUNTIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Marital Status */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Marital status</label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              { value: 'single', label: 'Single' },
              { value: 'married', label: 'Married' },
              { value: 'cohabiting', label: 'Cohabiting' },
              { value: 'separated', label: 'Separated' },
              { value: 'widowed', label: 'Widowed' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => updateProfile({ marital_status: opt.value as any })}
                className={`select-card py-3 ${profile.marital_status === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
