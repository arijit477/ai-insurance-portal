import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';
import { Notification } from '../../core/models/notification';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  private authService = inject(AuthService);
  private notificationService = inject(NotificationService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  userName = '';
  unreadCount = 0;
  notifications: Notification[] = [];
  showNotificationsDropdown = false;

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.authService.getProfile().subscribe({
        next: (user: any) => {
          this.userName = user.full_name || user.email;
          this.cdr.markForCheck();
        },
        error: (err: any) => {
          console.error('Failed to fetch profile in navbar:', err);
        }
      });

      this.loadUnreadCount();
    }
  }

  loadUnreadCount(): void {
    this.notificationService.getUnreadCount().subscribe({
      next: (res) => {
        this.unreadCount = res.unread_count;
        this.cdr.markForCheck();
      },
      error: (err) => console.error('Failed to load unread count:', err)
    });
  }

  toggleNotificationsDropdown(): void {
    this.showNotificationsDropdown = !this.showNotificationsDropdown;
    if (this.showNotificationsDropdown) {
      this.loadNotifications();
    }
    this.cdr.markForCheck();
  }

  loadNotifications(): void {
    this.notificationService.getNotifications().subscribe({
      next: (data) => {
        this.notifications = data;
        this.cdr.markForCheck();
      },
      error: (err) => console.error('Failed to load notifications:', err)
    });
  }

  markAsRead(notification: Notification, event: Event): void {
    event.stopPropagation();
    if (notification.is_read) return;

    this.notificationService.markAsRead(notification.id).subscribe({
      next: () => {
        notification.is_read = true;
        this.unreadCount = Math.max(0, this.unreadCount - 1);
        this.cdr.markForCheck();
      },
      error: (err) => console.error('Failed to mark notification as read:', err)
    });
  }

  markAllAsRead(event: Event): void {
    event.stopPropagation();
    this.notificationService.markAllAsRead().subscribe({
      next: () => {
        this.notifications.forEach(n => n.is_read = true);
        this.unreadCount = 0;
        this.cdr.markForCheck();
      },
      error: (err) => console.error('Failed to mark all as read:', err)
    });
  }

  onNotificationClick(notification: Notification): void {
    this.showNotificationsDropdown = false;

    if (!notification.is_read) {
      this.notificationService.markAsRead(notification.id).subscribe({
        next: () => {
          notification.is_read = true;
          this.unreadCount = Math.max(0, this.unreadCount - 1);
          this.cdr.markForCheck();
        }
      });
    }

    if (notification.claim_id) {
      this.router.navigate(['/claims', notification.claim_id]);
    } else {
      this.router.navigate(['/dashboard']);
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}

