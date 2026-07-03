import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink } from '@angular/router';

import { AIService } from '../../core/services/ai.service';

@Component({
  selector: 'app-ai-report',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './ai-report.html',
  styleUrl: './ai-report.css',
})
export class AiReport implements OnInit {
  private route = inject(ActivatedRoute);
  private aiService = inject(AIService);
  private cdr = inject(ChangeDetectorRef);

  claimId!: number;
  report: any;
  loading = true;
  error = '';

  ngOnInit(): void {
    this.claimId = Number(this.route.snapshot.paramMap.get('claimId'));
    this.loadReport();
  }

  loadReport(): void {
    this.loading = true;
    this.error = '';
    this.cdr.markForCheck();

    this.aiService.getReport(this.claimId).subscribe({
      next: (response) => {
        console.log('AI report loaded:', response);
        this.report = response;
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load AI report:', err);
        this.error =
          err.error?.detail ?? 'No AI analysis report found for this claim. Run analysis first.';
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  exportReport(): void {
    this.aiService.downloadReport(this.claimId).subscribe((blob) => {
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement('a');

      a.href = url;

      a.download = `AI_Report_${this.claimId}.pdf`;

      a.click();

      window.URL.revokeObjectURL(url);
    });
  }

  get maxConfidence(): number {
    if (this.report?.damage_analysis?.damages?.length > 0) {
      const confidences = this.report.damage_analysis.damages.map((d: any) => d.confidence || 0);
      return Math.max(...confidences);
    }
    return 0;
  }
}

