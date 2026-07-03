import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';
import { MatSnackBar } from '@angular/material/snack-bar';

import { PolicyDetails } from '../../../core/models/policy/policy-details';
import { Policy } from '../../../core/models/policy/policy';
import { PolicyService } from '../../../core/services/policy.service';

@Component({
  selector: 'app-policy-details',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatDividerModule,
  ],
  templateUrl: './policies-details.html',
  styleUrl: './policies-details.css',
})
export class PolicyDetailsComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private policyService = inject(PolicyService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  cancelling = false;
  policy!: PolicyDetails;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadPolicy(id);
  }

  loadPolicy(id: number): void {
    this.policyService.getPolicy(id).subscribe({
      next: (response: PolicyDetails) => {
        this.policy = response;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err: any) => {
        console.error(err);
        this.snackBar.open('Failed to load policy details.', 'Close', { duration: 3000 });
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  cancelPolicy(): void {
    if (!confirm('Are you sure you want to request cancellation for this policy?')) {
      return;
    }

    this.cancelling = true;
    this.cdr.markForCheck();

    this.policyService.cancelPolicy(this.policy.id).subscribe({
      next: (updatedPolicy: Policy) => {
        this.snackBar.open('Cancellation requested successfully.', 'Close', { duration: 3000 });
        // Reload details
        this.loadPolicy(this.policy.id);
      },
      error: (err: any) => {
        console.error(err);
        this.snackBar.open('Failed to cancel policy.', 'Close', { duration: 3000 });
        this.cancelling = false;
        this.cdr.markForCheck();
      },
    });
  }
}
