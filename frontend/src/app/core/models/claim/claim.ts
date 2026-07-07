import { ClaimStatus } from './claim-status';

export interface Claim {

  id: number;

  claim_number: string;

  customer_id: number;

  policy_id: number;

  title: string;

  description: string;

  claim_amount: number;

  status: ClaimStatus;

  submitted_at: string;

  updated_at: string;

  rejection_reason?: string;

  credit_date?: string;

}