import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API } from '../constants/api';

@Injectable({
  providedIn: 'root',
})
export class AdminService {
  private http = inject(HttpClient);

  /**
   * List all users (Admin only)
   */
  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${API.BASE_URL}/admin/users`);
  }

  /**
   * List all claims with customer and AI details (Admin only)
   */
  getClaims(): Observable<any[]> {
    return this.http.get<any[]>(`${API.BASE_URL}/admin/claims`);
  }

  /**
   * Create a new Agent account (Admin only)
   */
  createAgent(fullName: string, email: string, password: string): Observable<any> {
    const params = new HttpParams()
      .set('full_name', fullName)
      .set('email', email)
      .set('password', password);

    return this.http.post<any>(`${API.BASE_URL}/admin/agents`, null, { params });
  }

  /**
   * Delete a user account (Admin only)
   */
  deleteUser(userId: number): Observable<any> {
    return this.http.delete<any>(`${API.BASE_URL}/admin/users/${userId}`);
  }
}
