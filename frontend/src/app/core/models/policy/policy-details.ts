import { PolicyStatus } from './policy-status';

export interface PolicyDetails {

  id: number;

  policy_number: string;

  customer_name: string;

  customer_email: string;

  plan_name: string;

  category: string;

  premium_paid: number;

  coverage_amount: number;

  start_date: string;

  end_date: string;

  status: PolicyStatus;

}