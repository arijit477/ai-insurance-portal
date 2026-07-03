import { PolicyStatus } from './policy-status';

export interface Policy {

  id: number;

  policy_number: string;

  customer_id: number;

  plan_id: number;

  premium_paid: number;

  start_date: string;

  end_date: string;

  status: PolicyStatus;

  created_at: string;

  updated_at: string;

}