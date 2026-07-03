import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';
import { DashboardSummary } from '../models/dashboard/dashboard-summary';


@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  private http = inject(HttpClient);

  private readonly baseUrl = API.BASE_URL;

  getSummary(): Observable<DashboardSummary> {
    return this.http.get<DashboardSummary>(`${this.baseUrl}${API.API_V1}${API.DASHBOARD.SUMMARY}`);
  }
}
