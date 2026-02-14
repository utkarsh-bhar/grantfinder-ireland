'use client';

import { useProfileStore } from '@/stores/profileStore';

export default function StepTransportOther() {
  const { profile, updateProfile } = useProfileStore();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Almost done — a few more</h2>
      <p className="mt-1 text-sm text-gray-500">Last step! These help us find transport, farming, and landlord grants.</p>

      <div className="mt-6 space-y-5">
        {/* Vehicle */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Do you own a car? What type?
          </label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {[
              { value: 'petrol', label: '⛽ Petrol' },
              { value: 'diesel', label: '⛽ Diesel' },
              { value: 'hybrid', label: '🔋 Hybrid' },
              { value: 'electric', label: '⚡ Electric' },
              { value: 'none', label: '🚶 No car' },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => {
                  updateProfile({
                    vehicle_type: opt.value,
                    owns_vehicle: opt.value !== 'none',
                  });
                }}
                className={`select-card py-3 ${profile.vehicle_type === opt.value ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* EV Purchase */}
        {profile.vehicle_type !== 'electric' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Are you considering buying an electric vehicle?
            </label>
            <div className="flex gap-3">
              {[true, false].map((val) => (
                <button
                  key={String(val)}
                  onClick={() => updateProfile({ planning_ev_purchase: val })}
                  className={`select-card flex-1 py-3 ${profile.planning_ev_purchase === val ? 'select-card-active' : ''}`}
                >
                  <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Farmer */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Are you a farmer?</label>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ is_farmer: val })}
                className={`select-card flex-1 py-3 ${profile.is_farmer === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Landlord */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you a landlord with rental properties?
          </label>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ is_landlord: val })}
                className={`select-card flex-1 py-3 ${profile.is_landlord === val ? 'select-card-active' : ''}`}
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
