'use client';

import { useProfileStore } from '@/stores/profileStore';

export default function StepYourHome() {
  const { profile, updateProfile } = useProfileStore();
  const isOwner = profile.home_status === 'owner' || profile.home_status === 'landlord';
  const isRenter = profile.home_status === 'renter' || profile.home_status === 'local_authority_tenant';

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Your home</h2>
      <p className="mt-1 text-sm text-gray-500">This helps us find housing and energy grants for you.</p>

      <div className="mt-6 space-y-5">
        {/* Home Status */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Do you own or rent?</label>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: 'owner', label: '🏠 Owner', desc: 'I own my home' },
              { value: 'renter', label: '🔑 Renter', desc: 'I rent privately' },
              { value: 'local_authority_tenant', label: '🏘️ Council tenant', desc: 'Local authority' },
              { value: 'living_with_family', label: '👨‍👩‍👧 With family', desc: 'Living with family' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => updateProfile({ home_status: opt.value as any })}
                className={`select-card ${profile.home_status === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-lg">{opt.label.split(' ')[0]}</span>
                <span className="mt-1 text-sm font-medium">{opt.label.split(' ').slice(1).join(' ')}</span>
                <span className="text-xs text-gray-400">{opt.desc}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Owner-specific questions */}
        {isOwner && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">House type</label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'detached', label: 'Detached' },
                  { value: 'semi_detached', label: 'Semi-D' },
                  { value: 'terraced', label: 'Terraced' },
                  { value: 'apartment', label: 'Apartment' },
                  { value: 'bungalow', label: 'Bungalow' },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => updateProfile({ home_type: opt.value as any })}
                    className={`select-card py-3 ${profile.home_type === opt.value ? 'select-card-active' : ''}`}
                  >
                    <span className="text-sm font-medium">{opt.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Approximate year built</label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 1960, label: 'Pre-1977' },
                  { value: 1990, label: '1978-2005' },
                  { value: 2008, label: '2006-2010' },
                  { value: 2015, label: '2011-2020' },
                  { value: 2023, label: 'After 2021' },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => updateProfile({ home_year_built: opt.value })}
                    className={`select-card py-3 ${profile.home_year_built === opt.value ? 'select-card-active' : ''}`}
                  >
                    <span className="text-sm font-medium">{opt.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">BER rating (if known)</label>
              <select
                className="input"
                value={profile.ber_rating || ''}
                onChange={(e) => updateProfile({ ber_rating: e.target.value || undefined })}
              >
                <option value="">I don&apos;t know</option>
                {['A1','A2','A3','B1','B2','B3','C1','C2','C3','D1','D2','E1','E2','F','G'].map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Solar panels?</label>
                <div className="flex gap-3">
                  {[true, false].map((val) => (
                    <button
                      key={String(val)}
                      onClick={() => updateProfile({ has_solar_pv: val })}
                      className={`select-card flex-1 py-3 ${profile.has_solar_pv === val ? 'select-card-active' : ''}`}
                    >
                      <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Heat pump?</label>
                <div className="flex gap-3">
                  {[true, false].map((val) => (
                    <button
                      key={String(val)}
                      onClick={() => updateProfile({ has_heat_pump: val })}
                      className={`select-card flex-1 py-3 ${profile.has_heat_pump === val ? 'select-card-active' : ''}`}
                    >
                      <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}

        {/* First-time buyer */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Are you a first-time buyer?</label>
          <div className="flex gap-3">
            {[
              { value: true, label: 'Yes' },
              { value: false, label: 'No' },
            ].map((opt) => (
              <button
                key={String(opt.value)}
                onClick={() => updateProfile({ is_first_time_buyer: opt.value })}
                className={`select-card flex-1 py-3 ${profile.is_first_time_buyer === opt.value ? 'select-card-active' : ''}`}
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
