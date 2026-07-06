import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { AuthService } from '../../core/services/auth.service';
import { User } from '../../core/models/auth/user';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class ProfileComponent implements OnInit {
  private authService = inject(AuthService);
  private fb = inject(FormBuilder);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  user: User | null = null;
  loadingProfile = true;
  saving = false;
  error = '';

  hidePassword = true;
  hideConfirmPassword = true;

  profileForm = this.fb.group({
    full_name: ['', [Validators.required, Validators.minLength(3)]],
    password: ['', [Validators.minLength(8)]],
    confirm_password: [''],
  });

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.loadingProfile = true;
    this.error = '';
    this.cdr.markForCheck();

    this.authService.getProfile().subscribe({
      next: (user: User) => {
        this.user = user;
        this.profileForm.patchValue({
          full_name: user.full_name,
        });
        this.loadingProfile = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load profile:', err);
        this.error = 'Failed to load profile. Please reload the page.';
        this.loadingProfile = false;
        this.cdr.markForCheck();
      },
    });
  }

  save(): void {
    if (this.profileForm.invalid) {
      return;
    }

    const val = this.profileForm.getRawValue();
    const payload: { full_name?: string; password?: string } = {};

    if (val.full_name !== this.user?.full_name) {
      payload.full_name = val.full_name || undefined;
    }

    if (val.password) {
      if (val.password !== val.confirm_password) {
        this.snackBar.open('Passwords do not match.', 'Close', { duration: 3000 });
        return;
      }
      payload.password = val.password;
    }

    if (Object.keys(payload).length === 0) {
      this.snackBar.open('No changes to save.', 'Close', { duration: 3000 });
      return;
    }

    this.saving = true;
    this.cdr.markForCheck();

    this.authService.updateProfile(payload).subscribe({
      next: (updatedUser: User) => {
        this.user = updatedUser;
        this.snackBar.open('Profile updated successfully.', 'Close', { duration: 3000 });
        
        // Reset password fields
        this.profileForm.patchValue({
          password: '',
          confirm_password: '',
        });
        this.profileForm.get('password')?.markAsPristine();
        this.profileForm.get('password')?.markAsUntouched();
        this.profileForm.get('confirm_password')?.markAsPristine();
        this.profileForm.get('confirm_password')?.markAsUntouched();
        
        this.saving = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to update profile:', err);
        this.snackBar.open(err.error?.detail || 'Failed to update profile.', 'Close', { duration: 3000 });
        this.saving = false;
        this.cdr.markForCheck();
      },
    });
  }
}
