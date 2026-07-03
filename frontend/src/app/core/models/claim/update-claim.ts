import { ClaimStatus } from './claim-status';

export interface UpdateClaim {

  title?: string;

  description?: string;

  claim_amount?: number;

  status?: ClaimStatus;

}