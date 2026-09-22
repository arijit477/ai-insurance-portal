import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    MatListModule,
    MatIconModule,
    RouterLink,
    RouterLinkActive,
  ],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class Sidebar implements OnInit {
  private authService = inject(AuthService);
  private cdr = inject(ChangeDetectorRef);

  isAdminOrAgent = true;

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.authService.getProfile().subscribe({
        next: (user) => {
          this.isAdminOrAgent = user.role === 'Admin' || user.role === 'Agent';
          this.cdr.markForCheck();
        },
        error: (err) => {
          console.error('Failed to load profile in sidebar:', err);
        }
      });
    }
  }
}
