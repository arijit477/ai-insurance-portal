import { InsuranceCategory } from './insurance-category';

export interface InsurancePlan {

  id: number;

  plan_name: string;

  category: InsuranceCategory;

  premium: number;

  coverage_amount: number;

  duration_months: number;

  description: string;

  is_active: boolean;

  created_at: string;

  updated_at: string;

}