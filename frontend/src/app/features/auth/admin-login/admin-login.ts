import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './admin-login.html',
  styleUrl: './admin-login.css',
})
export class AdminLoginComponent {
  hidePassword = true;
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  loading = false;
  error = '';

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
  });

  login(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';
    this.cdr.markForCheck();

    const credentials = this.loginForm.getRawValue() as any;

    this.authService.login(credentials).subscribe({
      next: (response) => {
        // Save token first so profile query is authenticated
        this.authService.saveToken(response.access_token);

        // Fetch profile to verify role
        this.authService.getProfile().subscribe({
          next: (user) => {
            if (user && user.role === 'Admin') {
              this.router.navigate(['/admin']);
            } else {
              this.authService.logout();
              this.error = 'Access denied. Administrator privileges required.';
              this.loading = false;
              this.cdr.markForCheck();
            }
          },
          error: (err) => {
            console.error('Admin verification failed:', err);
            this.authService.logout();
            this.error = 'Verification failed. Please try again.';
            this.loading = false;
            this.cdr.markForCheck();
          }
        });
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail ?? 'Authentication failed';
        this.cdr.markForCheck();
      }
    });
  }
}
