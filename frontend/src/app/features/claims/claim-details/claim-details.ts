import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ClaimService } from '../../../core/services/claim.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ClaimBundleUploadComponent } from '../../upload/claim-bundle-upload/claim-bundle-upload';
import { AIService } from '../../../core/services/ai.service';
import { MatProgressBarModule } from "@angular/material/progress-bar";
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { UploadService } from '../../../core/services/upload.service';

@Component({
  selector: 'app-claim-details',
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatProgressSpinnerModule,
    ClaimBundleUploadComponent,
    MatProgressBarModule,
    MatButtonModule,
    MatIconModule
],
  templateUrl: './claim-details.html',
  styleUrl: './claim-details.css',
})
export class ClaimDetails implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  private claimService = inject(ClaimService);
  private aiService = inject(AIService);
  private uploadService = inject(UploadService);
  private cdr = inject(ChangeDetectorRef);
  analyzing = false;

  claim: any;

  loading = true;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.loadClaim(id);
  }

  loadClaim(id: number): void {
    this.claimService.getClaim(id).subscribe({
      next: (response) => {
        console.log('Claim details response:', response);
        this.claim = response;
        this.loading = false;
        this.cdr.markForCheck();
      },

      error: (err) => {
        console.error('Failed to load claim:', err);
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  analyzeClaim(): void {
    this.analyzing = true;
    this.cdr.markForCheck();

    this.aiService.analyzeClaim(this.claim.id).subscribe({
      next: () => {
        this.router.navigate(['/ai-reports']);
      },

      error: (err) => {
        console.error(err);
        this.analyzing = false;
        this.cdr.markForCheck();
      },
    });
  }

  deleteDocument(documentId: number): void {
    this.uploadService.deleteDocument(documentId).subscribe({
      next: () => {
        this.loadClaim(this.claim.id);
      },
      error: (err) => console.error('Failed to delete document:', err)
    });
  }

  deleteImage(imageId: number): void {
    this.uploadService.deleteImage(imageId).subscribe({
      next: () => {
        this.loadClaim(this.claim.id);
      },
      error: (err) => console.error('Failed to delete image:', err)
    });
  }

  clearAllFiles(): void {
    if (!confirm('Are you sure you want to clear all uploaded files?')) return;

    const deletePromises: Promise<any>[] = [];

    if (this.claim.documents) {
      for (const doc of this.claim.documents) {
        deletePromises.push(this.uploadService.deleteDocument(doc.id).toPromise());
      }
    }

    if (this.claim.images) {
      for (const img of this.claim.images) {
        deletePromises.push(this.uploadService.deleteImage(img.id).toPromise());
      }
    }

    Promise.all(deletePromises).then(() => {
      this.loadClaim(this.claim.id);
    }).catch(err => {
      console.error('Failed to clear some files:', err);
      this.loadClaim(this.claim.id);
    });
  }
}
