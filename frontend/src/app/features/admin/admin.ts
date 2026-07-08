import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
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
import { UploadService } from '../../core/services/upload.service';
import { Claim } from '../../core/models/claim/claim';
import { API } from '../../core/constants/api';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
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
  private uploadService = inject(UploadService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  loadingClaims = true;
  loadingUsers = true;
  creatingAgent = false;

  claimsDataSource = new MatTableDataSource<any>();
  usersDataSource = new MatTableDataSource<any>();

  selectedClaim: any = null;
  showApproveForm = false;
  showRejectForm = false;
  creditDate = '';
  rejectionReason = '';
  showDeleteConfirmModal = false;
  userToDelete: any = null;
  showFileDeleteConfirmModal = false;
  fileToDelete: any = null;
  fileDeleteType: 'document' | 'image' | null = null;

  claimColumns = [
    'claim_number',
    'customer',
    'title',
    'claim_amount',
    'ai_status',
    'status',
    'actions',
  ];

  userColumns = [
    'id',
    'full_name',
    'email',
    'role',
    'status',
    'actions',
  ];

  agentForm = this.fb.group({
    full_name: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  ngOnInit(): void {
    this.loadClaims();
    this.loadUsers();
  }

  loadClaims(): void {
    this.loadingClaims = true;
    this.cdr.markForCheck();

    this.adminService.getClaims().subscribe({
      next: (response) => {
        this.claimsDataSource.data = response;
        this.loadingClaims = false;
        if (this.selectedClaim) {
          const updated = response.find(c => c.id === this.selectedClaim.id);
          this.selectedClaim = updated || null;
        }
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

  selectClaim(claim: any): void {
    this.selectedClaim = claim;
    this.showApproveForm = false;
    this.showRejectForm = false;
    this.creditDate = '';
    this.rejectionReason = '';
    this.cdr.markForCheck();
  }

  closeDrawer(): void {
    this.selectedClaim = null;
    this.showApproveForm = false;
    this.showRejectForm = false;
    this.creditDate = '';
    this.rejectionReason = '';
    this.cdr.markForCheck();
  }

  get maxConfidence(): number {
    if (this.selectedClaim?.ai_report?.damage_analysis?.damages?.length > 0) {
      const confidences = this.selectedClaim.ai_report.damage_analysis.damages.map((d: any) => d.confidence || 0);
      return Math.max(...confidences);
    }
    return 0;
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

  confirmApprove(): void {
    if (!this.creditDate) {
      this.snackBar.open('Please select an insurance credit date.', 'Close', { duration: 3000 });
      return;
    }
    const isoDate = new Date(this.creditDate).toISOString();
    this.claimService.approveClaim(this.selectedClaim.id, { credit_date: isoDate }).subscribe({
      next: () => {
        this.snackBar.open('Claim approved successfully.', 'Close', { duration: 3000 });
        this.showApproveForm = false;
        this.creditDate = '';
        this.loadClaims();
      },
      error: (err) => {
        console.error(err);
        this.snackBar.open('Failed to approve claim.', 'Close', { duration: 3000 });
      },
    });
  }

  confirmReject(): void {
    if (!this.rejectionReason.trim()) {
      this.snackBar.open('Please enter a rejection reason.', 'Close', { duration: 3000 });
      return;
    }
    this.claimService.rejectClaim(this.selectedClaim.id, { rejection_reason: this.rejectionReason }).subscribe({
      next: () => {
        this.snackBar.open('Claim rejected successfully.', 'Close', { duration: 3000 });
        this.showRejectForm = false;
        this.rejectionReason = '';
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

  deleteUser(user: any): void {
    this.userToDelete = user;
    this.showDeleteConfirmModal = true;
    this.cdr.markForCheck();
  }

  cancelDelete(): void {
    this.showDeleteConfirmModal = false;
    this.userToDelete = null;
    this.cdr.markForCheck();
  }

  confirmDelete(): void {
    if (!this.userToDelete) return;

    this.adminService.deleteUser(this.userToDelete.id).subscribe({
      next: (res) => {
        this.snackBar.open(res.message || 'User account deleted successfully.', 'Close', { duration: 3000 });
        this.showDeleteConfirmModal = false;
        this.userToDelete = null;
        this.loadUsers();
      },
      error: (err) => {
        console.error('Failed to delete user:', err);
        this.snackBar.open(err.error?.detail || 'Failed to delete user account.', 'Close', { duration: 3000 });
        this.showDeleteConfirmModal = false;
        this.userToDelete = null;
        this.cdr.markForCheck();
      }
    });
  }

  deleteDocument(doc: any): void {
    this.fileToDelete = doc;
    this.fileDeleteType = 'document';
    this.showFileDeleteConfirmModal = true;
    this.cdr.markForCheck();
  }

  deleteImage(img: any): void {
    this.fileToDelete = img;
    this.fileDeleteType = 'image';
    this.showFileDeleteConfirmModal = true;
    this.cdr.markForCheck();
  }

  cancelFileDelete(): void {
    this.showFileDeleteConfirmModal = false;
    this.fileToDelete = null;
    this.fileDeleteType = null;
    this.cdr.markForCheck();
  }

  confirmFileDelete(): void {
    if (!this.fileToDelete || !this.fileDeleteType) return;

    if (this.fileDeleteType === 'document') {
      this.uploadService.deleteDocument(this.fileToDelete.id).subscribe({
        next: () => {
          this.snackBar.open('Document deleted successfully.', 'Close', { duration: 3000 });
          this.showFileDeleteConfirmModal = false;
          
          if (this.selectedClaim) {
            this.selectedClaim.documents = this.selectedClaim.documents.filter((d: any) => d.id !== this.fileToDelete.id);
          }
          this.fileToDelete = null;
          this.fileDeleteType = null;
          this.loadClaims();
        },
        error: (err) => {
          console.error(err);
          this.snackBar.open('Failed to delete document.', 'Close', { duration: 3000 });
          this.showFileDeleteConfirmModal = false;
          this.fileToDelete = null;
          this.fileDeleteType = null;
          this.cdr.markForCheck();
        }
      });
    } else if (this.fileDeleteType === 'image') {
      this.uploadService.deleteImage(this.fileToDelete.id).subscribe({
        next: () => {
          this.snackBar.open('Image deleted successfully.', 'Close', { duration: 3000 });
          this.showFileDeleteConfirmModal = false;
          
          if (this.selectedClaim) {
            this.selectedClaim.images = this.selectedClaim.images.filter((i: any) => i.id !== this.fileToDelete.id);
          }
          this.fileToDelete = null;
          this.fileDeleteType = null;
          this.loadClaims();
        },
        error: (err) => {
          console.error(err);
          this.snackBar.open('Failed to delete image.', 'Close', { duration: 3000 });
          this.showFileDeleteConfirmModal = false;
          this.fileToDelete = null;
          this.fileDeleteType = null;
          this.cdr.markForCheck();
        }
      });
    }
  }

  // getFileUrl(filePath: string): string {
  //   if (!filePath) return '';
  //   const normalized = filePath.replace(/\\/g, '/');
  //   return `${API.BASE_URL}/${normalized}`;
  // }

    getFileUrl(filePath: string): string {
    if (!filePath) return '';
    // If the path is already a cloud URL, return it directly!
    if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
      return filePath;
    }
    // Fallback for older local relative uploads
    const normalized = filePath.replace(/\\/g, '/');
    return `${API.BASE_URL}/${normalized}`;
  }

}
