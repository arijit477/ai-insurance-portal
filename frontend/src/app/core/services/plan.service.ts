import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

import { InsurancePlan } from '../models/insurance/insurance-plan';
import { CreateInsurancePlan } from '../models/insurance/create-insurance-plan';
import { UpdateInsurancePlan } from '../models/insurance/update-insurance-plan';

@Injectable({
  providedIn: 'root',
})
export class PlanService {

  private http = inject(HttpClient);

  /**
   * Get all insurance plans
   */
  getPlans(): Observable<InsurancePlan[]> {

    return this.http.get<InsurancePlan[]>(
      `${API.BASE_URL}${API.PLANS.LIST}`
    );

  }

  /**
   * Get plan details
   */
  getPlan(
    planId: number,
  ): Observable<InsurancePlan> {

    return this.http.get<InsurancePlan>(
      `${API.BASE_URL}${API.PLANS.DETAILS}/${planId}`
    );

  }

  /**
   * Create plan (Admin)
   */
  createPlan(
    request: CreateInsurancePlan,
  ): Observable<InsurancePlan> {

    return this.http.post<InsurancePlan>(
      `${API.BASE_URL}${API.PLANS.CREATE}`,
      request,
    );

  }

  /**
   * Update plan (Admin)
   */
  updatePlan(
    planId: number,
    request: UpdateInsurancePlan,
  ): Observable<InsurancePlan> {

    return this.http.put<InsurancePlan>(
      `${API.BASE_URL}${API.PLANS.UPDATE}/${planId}`,
      request,
    );

  }

  /**
   * Delete plan (Admin)
   */
  deletePlan(
    planId: number,
  ): Observable<void> {

    return this.http.delete<void>(
      `${API.BASE_URL}${API.PLANS.DELETE}/${planId}`
    );

  }

}