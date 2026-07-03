import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { MatTabsModule } from '@angular/material/tabs';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';

import { ClaimService } from '../../core/services/claim.service';
import { AdminService } from '../../core/services/admin.service';
import { Claim } from '../../core/models/claim/claim';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    MatTabsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatCardModule,
  ],
  templateUrl: './admin.html',
  styleUrl: './admin.css',
})
export class Admin implements OnInit {
  private fb = inject(FormBuilder);
  private claimService = inject(ClaimService);
  private adminService = inject(AdminService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  loadingClaims = true;
  loadingUsers = true;
  creatingAgent = false;

  claimsDataSource = new MatTableDataSource<Claim>();
  usersDataSource = new MatTableDataSource<any>();

  claimColumns = [
    'claim_number',
    'title',
    'claim_amount',
    'status',
    'actions',
  ];

  userColumns = [
    'id',
    'full_name',
    'email',
    'role',
    'status',
  ];

  agentForm = this.fb.group({
    full_name: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  ngOnInit(): void {
    this.loadClaims();
    this.loadUsers();
  }

  loadClaims(): void {
    this.loadingClaims = true;
    this.cdr.markForCheck();

    this.claimService.getAllClaims().subscribe({
      next: (response) => {
        this.claimsDataSource.data = response;
        this.loadingClaims = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load all claims:', err);
        this.snackBar.open('Failed to load claims database.', 'Close', { duration: 3000 });
        this.loadingClaims = false;
        this.cdr.markForCheck();
      },
    });
  }

  loadUsers(): void {
    this.loadingUsers = true;
    this.cdr.markForCheck();

    this.adminService.getUsers().subscribe({
      next: (response) => {
        this.usersDataSource.data = response;
        this.loadingUsers = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load users:', err);
        this.snackBar.open('Failed to load users database.', 'Close', { duration: 3000 });
        this.loadingUsers = false;
        this.cdr.markForCheck();
      },
    });
  }

  approveClaim(id: number): void {
    this.claimService.approveClaim(id).subscribe({
      next: () => {
        this.snackBar.open('Claim approved successfully.', 'Close', { duration: 3000 });
        this.loadClaims();
      },
      error: (err) => {
        console.error(err);
        this.snackBar.open('Failed to approve claim.', 'Close', { duration: 3000 });
      },
    });
  }

  rejectClaim(id: number): void {
    this.claimService.rejectClaim(id).subscribe({
      next: () => {
        this.snackBar.open('Claim rejected successfully.', 'Close', { duration: 3000 });
        this.loadClaims();
      },
      error: (err) => {
        console.error(err);
        this.snackBar.open('Failed to reject claim.', 'Close', { duration: 3000 });
      },
    });
  }

  onCreateAgentSubmit(): void {
    if (this.agentForm.invalid) {
      return;
    }

    this.creatingAgent = true;
    this.cdr.markForCheck();

    const rawForm = this.agentForm.getRawValue();
    this.adminService.createAgent(
      rawForm.full_name!,
      rawForm.email!,
      rawForm.password!
    ).subscribe({
      next: () => {
        this.snackBar.open('Agent created successfully.', 'Close', { duration: 3000 });
        this.agentForm.reset();
        this.creatingAgent = false;
        this.loadUsers();
      },
      error: (err) => {
        console.error(err);
        this.snackBar.open(err.error?.detail ?? 'Failed to create agent account.', 'Close', { duration: 3000 });
        this.creatingAgent = false;
        this.cdr.markForCheck();
      },
    });
  }
}
