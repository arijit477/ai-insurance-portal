import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';

import { InsurancePlan } from '../../../core/models/insurance/insurance-plan';
import { PlanService } from '../../../core/services/plan.service';
import { PolicyService } from '../../../core/services/policy.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-plan-details',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatDividerModule,
  ],
  templateUrl: './plan-details.html',
  styleUrl: './plan-details.css',
})
export class PlanDetailsComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private planService = inject(PlanService);
  private policyService = inject(PolicyService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  purchasing = false;
  plan!: InsurancePlan;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadPlan(id);
  }

  loadPlan(id: number): void {
    this.planService.getPlan(id).subscribe({
      next: (response) => {
        this.plan = response;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  purchasePolicy(): void {
    this.purchasing = true;
    this.cdr.markForCheck();

    this.policyService.createPolicy({ plan_id: this.plan.id }).subscribe({
      next: () => {
        this.snackBar.open('Policy purchased successfully!', 'Close', { duration: 3000 });
        this.router.navigate(['/policies']);
      },
      error: (err) => {
        console.error(err);
        this.purchasing = false;
        this.cdr.markForCheck();
      },
    });
  }
}
