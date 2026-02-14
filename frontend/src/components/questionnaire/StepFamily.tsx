'use client';

import { useProfileStore } from '@/stores/profileStore';

export default function StepFamily() {
  const { profile, updateProfile } = useProfileStore();

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900">Your family</h2>
      <p className="mt-1 text-sm text-gray-500">Family details help us find child, carer, and family grants.</p>

      <div className="mt-6 space-y-5">
        {/* Has Children */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Do you have children?</label>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ has_children: val })}
                className={`select-card flex-1 py-3 ${profile.has_children === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Children details */}
        {profile.has_children && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">How many children?</label>
              <input
                type="number"
                className="input"
                min={1}
                max={20}
                value={profile.num_children || ''}
                onChange={(e) => updateProfile({ num_children: e.target.value ? Number(e.target.value) : undefined })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Age of youngest child</label>
              <input
                type="number"
                className="input"
                min={0}
                max={25}
                value={profile.youngest_child_age ?? ''}
                onChange={(e) => updateProfile({ youngest_child_age: e.target.value ? Number(e.target.value) : undefined })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Are you a lone parent?</label>
              <div className="flex gap-3">
                {[true, false].map((val) => (
                  <button
                    key={String(val)}
                    onClick={() => updateProfile({ is_lone_parent: val })}
                    className={`select-card flex-1 py-3 ${profile.is_lone_parent === val ? 'select-card-active' : ''}`}
                  >
                    <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
                  </button>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Carer */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Are you caring for someone? (elderly parent, person with disability, etc.)
          </label>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ is_carer: val })}
                className={`select-card flex-1 py-3 ${profile.is_carer === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Dependent Relatives */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Do you financially support a dependent relative?
          </label>
          <p className="text-xs text-gray-400 mb-2">
            e.g. a parent aged 65+, a widowed parent, or a relative unable to support themselves due to age/infirmity
          </p>
          <div className="flex gap-3">
            {[true, false].map((val) => (
              <button
                key={String(val)}
                onClick={() => updateProfile({ has_dependent_relatives: val, ...(val ? {} : { num_dependent_relatives: undefined }) })}
                className={`select-card flex-1 py-3 ${profile.has_dependent_relatives === val ? 'select-card-active' : ''}`}
              >
                <span className="text-sm font-medium">{val ? 'Yes' : 'No'}</span>
              </button>
            ))}
          </div>
        </div>

        {profile.has_dependent_relatives && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">How many dependent relatives?</label>
            <input
              type="number"
              className="input"
              min={1}
              max={10}
              value={profile.num_dependent_relatives || ''}
              onChange={(e) => updateProfile({ num_dependent_relatives: e.target.value ? Number(e.target.value) : undefined })}
            />
          </div>
        )}

        {/* Incapacitated Child */}
        {profile.has_children && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Does any of your children have a permanent incapacity (physical or mental)?
            </label>
            <p className="text-xs text-gray-400 mb-2">
              This may qualify you for the Incapacitated Child Tax Credit of €3,800 per child
            </p>
            <div className="flex gap-3">
              {[true, false].map((val) => (
                <button
                  key={String(val)}
                  onClick={() => updateProfile({ has_incapacitated_child: val })}
                  className={`select-card flex-1 py-3 ${profile.has_incapacitated_child === val ? 'select-card-active' : ''}`}
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
