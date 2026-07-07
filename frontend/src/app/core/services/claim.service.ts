import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

import { Claim } from '../models/claim/claim';
import { ClaimDetails } from '../models/claim/claim-details';
import { CreateClaim } from '../models/claim/create-claim';
import { UpdateClaim } from '../models/claim/update-claim';

@Injectable({
  providedIn: 'root',
})
export class ClaimService {

  private http = inject(HttpClient);

  getClaims(): Observable<Claim[]> {

    return this.http.get<Claim[]>(
      `${API.BASE_URL}${API.CLAIMS.MY}`
    );

  }

  getClaim(
    claimId: number,
  ): Observable<ClaimDetails> {

    return this.http.get<ClaimDetails>(
      `${API.BASE_URL}${API.CLAIMS.DETAILS}/${claimId}`
    );

  }

  createClaim(
    request: CreateClaim,
  ): Observable<Claim> {

    return this.http.post<Claim>(
      `${API.BASE_URL}${API.CLAIMS.CREATE}`,
      request,
    );

  }

  /**
   * Get all claims in the system (Admin/Agent only)
   */
  getAllClaims(): Observable<Claim[]> {
    return this.http.get<Claim[]>(
      `${API.BASE_URL}${API.CLAIMS.LIST}`
    );
  }

  /**
   * Approve a claim (Admin only)
   */
  approveClaim(claimId: number, payload: { credit_date: string }): Observable<Claim> {
    return this.http.put<Claim>(
      `${API.BASE_URL}/claims/${claimId}/approve`,
      payload
    );
  }

  /**
   * Reject a claim (Admin only)
   */
  rejectClaim(claimId: number, payload: { rejection_reason: string }): Observable<Claim> {
    return this.http.put<Claim>(
      `${API.BASE_URL}/claims/${claimId}/reject`,
      payload
    );
  }

  updateClaim(
    claimId: number,
    request: UpdateClaim,
  ): Observable<Claim> {

    return this.http.put<Claim>(
      `${API.BASE_URL}${API.CLAIMS.UPDATE}/${claimId}`,
      request,
    );

  }

  deleteClaim(
    claimId: number,
  ): Observable<void> {

    return this.http.delete<void>(
      `${API.BASE_URL}${API.CLAIMS.DELETE}/${claimId}`
    );

  }

}