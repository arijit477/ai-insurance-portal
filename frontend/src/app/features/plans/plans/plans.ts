import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { InsurancePlan } from '../../../core/models/insurance/insurance-plan';
import { PlanService } from '../../../core/services/plan.service';

@Component({
  selector: 'app-plans',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './plans.html',
  styleUrl: './plans.css',
})
export class PlansComponent implements OnInit {

  private planService = inject(PlanService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  plans: InsurancePlan[] = [];

  ngOnInit(): void {
    this.loadPlans();
  }

  loadPlans(): void {
    this.planService.getPlans().subscribe({
      next: (plans) => {
        this.plans = plans;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  viewPlan(id: number): void {
    this.router.navigate(['/plans', id]);
  }
}