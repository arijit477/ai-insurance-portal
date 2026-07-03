import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

import { DashboardService } from '../../core/services/dashboard.service';
import { DashboardSummary } from '../../core/models/dashboard/dashboard-summary';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class DashboardComponent implements OnInit {

  private dashboardService = inject(DashboardService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  error = '';

  dashboard: DashboardSummary = {
    active_policies: 0,
    total_claims: 0,
    pending_claims: 0,
    approved_claims: 0,
    rejected_claims: 0,
    ai_reports: 0,
  };

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.dashboardService.getSummary().subscribe({
      next: (response) => {
        this.dashboard = response;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error(err);
        this.error = 'Unable to load dashboard.';
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  createClaim(): void {
    this.router.navigate(['/claims/create']);
  }

  uploadDocuments(): void {
    this.router.navigate(['/claims/create']);
  }

  viewAiReports(): void {
    this.router.navigate(['/ai-reports']);
  }

  browsePlans(): void {
    this.router.navigate(['/plans']);
  }
}
