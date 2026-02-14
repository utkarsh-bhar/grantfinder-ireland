// ─── Profile / Questionnaire Types ──────────────────────────────────────────

export interface ProfileData {
  // Step 1: About You
  age?: number;
  county?: string;
  marital_status?: 'single' | 'married' | 'cohabiting' | 'separated' | 'widowed';
  nationality?: string;
  residency_status?: string;

  // Step 2: Your Home
  home_status?: 'owner' | 'renter' | 'local_authority_tenant' | 'living_with_family' | 'homeless' | 'landlord';
  home_type?: 'detached' | 'semi_detached' | 'terraced' | 'apartment' | 'bungalow';
  home_year_built?: number;
  ber_rating?: string;
  has_solar_pv?: boolean;
  has_heat_pump?: boolean;
  is_first_time_buyer?: boolean;
  has_mortgage?: boolean;
  pays_rent?: boolean;

  // Step 3: Family
  has_children?: boolean;
  num_children?: number;
  youngest_child_age?: number;
  is_lone_parent?: boolean;
  is_carer?: boolean;
  has_dependent_relatives?: boolean;
  num_dependent_relatives?: number;
  has_incapacitated_child?: boolean;

  // Step 4: Work & Income
  employment_status?: 'employed' | 'self_employed' | 'unemployed' | 'retired' | 'student' | 'homemaker';
  income_bracket?: '<20k' | '20-40k' | '40-60k' | '60-80k' | '80k+';
  is_freelancer?: boolean;
  works_from_home?: boolean;

  // Step 5: Welfare & Health
  welfare_payments?: string[];
  has_medical_card?: boolean;
  has_disability?: boolean;
  household_disability?: boolean;
  has_medical_expenses?: boolean;
  is_visually_impaired?: boolean;
  has_nursing_home_expenses?: boolean;

  // Step 6: Education & Business
  is_student?: boolean;
  planning_education?: boolean;
  owns_business?: boolean;
  planning_business?: boolean;
  business_age_months?: number;
  num_employees?: number;

  // Step 7: Transport & Other
  owns_vehicle?: boolean;
  vehicle_type?: string;
  planning_ev_purchase?: boolean;
  is_farmer?: boolean;
  is_landlord?: boolean;
}

// ─── Scan / Results Types ───────────────────────────────────────────────────

export interface GrantMatch {
  grant_id: string;
  name: string;
  slug: string;
  short_description: string;
  match_type: 'eligible' | 'likely' | 'possible';
  match_score: number;
  max_amount: number | null;
  amount_description: string;
  source_organisation: string;
  source_url: string;
  application_url: string | null;
  notes: string;
  is_locked: boolean;
  category: string;
  estimated_annual_saving: number | null;
  estimated_backdated_saving: number | null;
  savings_note: string;
  how_to_claim: string;
}

export interface CategoryResult {
  category: string;
  label: string;
  count: number;
  total_value: number;
  grants: GrantMatch[];
}

export interface ScanResponse {
  scan_id: string | null;
  total_grants_found: number;
  total_potential_value: number;
  categories: CategoryResult[];
  summary: string;
  generated_at: string;
}

// ─── Grant Types ────────────────────────────────────────────────────────────

export interface Grant {
  id: string;
  name: string;
  slug: string;
  short_description: string;
  long_description?: string;
  category: string;
  subcategory?: string;
  max_amount: number | null;
  amount_description?: string;
  amount_type: string;
  is_means_tested: boolean;
  source_organisation: string;
  source_url: string;
  application_url?: string;
  application_method?: string;
  is_always_open: boolean;
  closing_date?: string;
  typical_processing?: string;
  is_active: boolean;
  last_verified_at: string;
  created_at: string;
}

export interface GrantStep {
  id: string;
  step_number: number;
  title: string;
  description: string;
  url?: string;
}

export interface GrantDocument {
  id: string;
  document_name: string;
  description?: string;
  is_required: boolean;
}

// ─── Auth Types ─────────────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  plan: 'free' | 'report' | 'premium';
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// ─── Constants ──────────────────────────────────────────────────────────────

export const IRISH_COUNTIES = [
  'Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal', 'Dublin',
  'Galway', 'Kerry', 'Kildare', 'Kilkenny', 'Laois', 'Leitrim',
  'Limerick', 'Longford', 'Louth', 'Mayo', 'Meath', 'Monaghan',
  'Offaly', 'Roscommon', 'Sligo', 'Tipperary', 'Waterford',
  'Westmeath', 'Wexford', 'Wicklow',
] as const;

export const WELFARE_PAYMENT_OPTIONS = [
  { value: 'fuel_allowance', label: 'Fuel Allowance' },
  { value: 'disability_allowance', label: 'Disability Allowance' },
  { value: 'jobseekers_allowance', label: "Jobseeker's Allowance" },
  { value: 'working_family_payment', label: 'Working Family Payment' },
  { value: 'carers_allowance', label: "Carer's Allowance" },
  { value: 'one_parent_family_payment', label: 'One Parent Family Payment' },
  { value: 'domiciliary_care_allowance', label: 'Domiciliary Care Allowance' },
  { value: 'state_pension', label: 'State Pension' },
  { value: 'invalidity_pension', label: 'Invalidity Pension' },
] as const;

export const CATEGORY_LABELS: Record<string, string> = {
  home_energy: 'Home Energy',
  housing: 'Housing',
  housing_support: 'Housing Support',
  welfare: 'Welfare & Social',
  business: 'Business',
  education: 'Education',
  health: 'Health',
  family: 'Family',
  disability: 'Disability',
  carers: 'Carers',
  transport: 'Transport',
  farming: 'Farming',
  community: 'Community',
  tax_relief: 'Tax Relief',
  employment: 'Employment',
};

export const CATEGORY_ICONS: Record<string, string> = {
  home_energy: '⚡',
  housing: '🏠',
  housing_support: '🏘️',
  welfare: '🤝',
  business: '💼',
  education: '🎓',
  health: '🏥',
  family: '👨‍👩‍👧‍👦',
  disability: '♿',
  carers: '❤️',
  transport: '🚗',
  farming: '🌾',
  community: '🏘️',
  tax_relief: '💰',
  employment: '👔',
};
