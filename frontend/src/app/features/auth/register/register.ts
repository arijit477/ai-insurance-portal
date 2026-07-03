import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
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
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class RegisterComponent {
  hidePassword = true;
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  loading = false;
  error = '';
  success = '';

  registerForm = this.fb.group({
    full_name: [
      '',
      [
        Validators.required,
        Validators.minLength(3),
      ],
    ],
    email: [
      '',
      [
        Validators.required,
        Validators.email,
      ],
    ],
    password: [
      '',
      [
        Validators.required,
        Validators.minLength(6),
      ],
    ],
  });

  register(): void {
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';
    this.success = '';
    this.cdr.markForCheck();

    this.authService.register(
      this.registerForm.getRawValue() as any
    )
    .subscribe({
      next: () => {
        this.loading = false;
        this.success = 'Registration successful!';
        this.cdr.markForCheck();

        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1500);
      },
      error: (err) => {
        this.loading = false;
        this.error =
          err.error?.detail ??
          'Registration failed';
        this.cdr.markForCheck();
      }
    });
  }
}