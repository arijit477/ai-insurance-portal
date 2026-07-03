import { InsuranceCategory } from './insurance-category';

export interface UpdateInsurancePlan {

  plan_name?: string;

  category?: InsuranceCategory;

  premium?: number;

  coverage_amount?: number;

  duration_months?: number;

  description?: string;

  is_active?: boolean;

}