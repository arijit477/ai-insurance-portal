import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';

import { AIService } from '../../../core/services/ai.service';

@Component({
  selector: 'app-ai-reports-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatButtonModule,
    MatChipsModule,
  ],
  templateUrl: './ai-reports-list.html',
  styleUrl: './ai-reports-list.css',
})
export class AiReportsList implements OnInit {
  private aiService = inject(AIService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  reports: any[] = [];
  loading = true;
  error = '';

  ngOnInit(): void {
    this.loadReports();
  }

  loadReports(): void {
    this.loading = true;
    this.error = '';

    this.aiService.getMyReports().subscribe({
      next: (data) => {
        this.reports = data;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load AI reports:', err);
        this.error = err.error?.detail ?? 'Failed to load AI reports.';
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  viewReport(report: any): void {
    this.router.navigate(['/ai-report', report.claim_id]);
  }

  getFraudClass(score: number): string {
    if (score > 70) return 'risk-high';
    if (score >= 30) return 'risk-med';
    return 'risk-low';
  }

  getFraudLabel(score: number): string {
    if (score > 70) return 'High Risk';
    if (score >= 30) return 'Medium Risk';
    return 'Low Risk';
  }

  getFraudIcon(score: number): string {
    if (score > 70) return 'gpp_bad';
    if (score >= 30) return 'gpp_maybe';
    return 'verified_user';
  }

  getScoreArcStyle(score: number): string {
    // returns inline style for the SVG arc progress
    const pct = Math.min(Math.max(score, 0), 100);
    return `stroke-dasharray: ${pct} ${100 - pct}`;
  }
}
