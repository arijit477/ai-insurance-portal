import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API } from '../constants/api';
import { Notification } from '../models/notification';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private http = inject(HttpClient);

  getNotifications(): Observable<Notification[]> {
    return this.http.get<Notification[]>(`${API.BASE_URL}${API.NOTIFICATIONS.LIST}`);
  }

  getUnreadCount(): Observable<{ unread_count: number }> {
    return this.http.get<{ unread_count: number }>(`${API.BASE_URL}${API.NOTIFICATIONS.UNREAD_COUNT}`);
  }

  markAsRead(notificationId: number): Observable<Notification> {
    return this.http.post<Notification>(`${API.BASE_URL}${API.NOTIFICATIONS.READ}/${notificationId}/read`, {});
  }

  markAllAsRead(): Observable<any> {
    return this.http.post<any>(`${API.BASE_URL}${API.NOTIFICATIONS.READ_ALL}`, {});
  }
}
