import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { API } from '../constants/api';

@Injectable({
  providedIn: 'root',
})
export class AIService {
  private http = inject(HttpClient);

  analyzeClaim(claimId: number): Observable<any> {
    return this.http.post(
      `${API.BASE_URL}${API.AI.ANALYZE}/${claimId}`,
      {},
    );
  }

  getReport(claimId: number): Observable<any> {
    return this.http.get(`${API.BASE_URL}${API.AI.REPORT}/${claimId}`);
  }

  /** Returns all AI reports belonging to the current user's claims. */
  getMyReports(): Observable<any[]> {
    return this.http.get<any[]>(`${API.BASE_URL}${API.AI.MY_REPORTS}`);
  }

  /** Admin: returns every AI report in the system. */
  getAllReports(): Observable<any[]> {
    return this.http.get<any[]>(`${API.BASE_URL}${API.AI.ALL_REPORTS}`);
  }

  downloadReport(claimId: number) {
    return this.http.get(
      `${API.BASE_URL}${API.AI.REPORT}/${claimId}/pdf`,
      {
        responseType: 'blob',
      },
    );
  }
}
