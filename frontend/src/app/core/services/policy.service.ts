import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

import { Policy } from '../models/policy/policy';
import { PolicyDetails } from '../models/policy/policy-details';
import { CreatePolicy } from '../models/policy/create-policy';

@Injectable({
  providedIn: 'root',
})
export class PolicyService {

  private http = inject(HttpClient);

  /**
   * Get all policies for the logged-in user
   */
  getPolicies(): Observable<Policy[]> {

    return this.http.get<Policy[]>(
      `${API.BASE_URL}${API.POLICIES.MY}`
    );

  }

  /**
   * Get policy details
   */
  getPolicy(
    policyId: number,
  ): Observable<PolicyDetails> {

    return this.http.get<PolicyDetails>(
      `${API.BASE_URL}${API.POLICIES.DETAILS}/${policyId}`
    );

  }

  /**
   * Purchase a new policy
   */
  createPolicy(
    request: CreatePolicy,
  ): Observable<Policy> {

    return this.http.post<Policy>(
      `${API.BASE_URL}${API.POLICIES.CREATE}`,
      request,
    );

  }

  /**
   * Update policy status
   */
  updatePolicy(
    policyId: number,
    status: string,
  ): Observable<Policy> {

    return this.http.put<Policy>(
      `${API.BASE_URL}${API.POLICIES.UPDATE}/${policyId}`,
      {
        status,
      },
    );

  }

  /**
   * Request cancellation for a policy
   */
  cancelPolicy(policyId: number): Observable<Policy> {
    return this.http.put<Policy>(
      `${API.BASE_URL}${API.POLICIES.DETAILS}/${policyId}/cancel`,
      {}
    );
  }

  /**
   * Cancel/Delete Policy
   */
  deletePolicy(
    policyId: number,
  ): Observable<void> {

    return this.http.delete<void>(
      `${API.BASE_URL}${API.POLICIES.DELETE}/${policyId}`
    );

  }

}