import { InsuranceCategory } from './insurance-category';

export interface CreateInsurancePlan {

  plan_name: string;

  category: InsuranceCategory;

  premium: number;

  coverage_amount: number;

  duration_months: number;

  description: string;

}