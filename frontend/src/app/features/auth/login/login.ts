import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
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
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
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

    this.authService.login(
      this.loginForm.getRawValue() as any
    )
    .subscribe({
      next: (response) => {
        this.authService.saveToken(
          response.access_token
        );
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.loading = false;
        this.error =
          err.error?.detail ??
          'Login failed';
        this.cdr.markForCheck();
      }
    });
  }
}