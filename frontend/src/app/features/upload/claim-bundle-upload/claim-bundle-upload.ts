import { Component, Input, Output, EventEmitter, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';

import { UploadService } from '../../../core/services/upload.service';

@Component({
  selector: 'app-claim-bundle-upload',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './claim-bundle-upload.html',
  styleUrl: './claim-bundle-upload.css',
})
export class ClaimBundleUploadComponent {
  @Input()
  claimId!: number;

  @Output()
  uploadComplete = new EventEmitter<void>();

  private uploadService = inject(UploadService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  selectedDocumentFile?: File;
  selectedImageFile?: File;

  preview?: string;

  uploading = false;
  uploaded = false;

  onDocumentSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (!input.files?.length) return;

    this.selectedDocumentFile = input.files[0];
  }

  onImageSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (!input.files?.length) return;

    this.selectedImageFile = input.files[0];

    const reader = new FileReader();
    reader.onload = () => {
      this.preview = reader.result as string;
    };
    reader.readAsDataURL(this.selectedImageFile);
  }

  async uploadBundle(): Promise<void> {
    if (!this.selectedDocumentFile && !this.selectedImageFile) return;

    this.uploading = true;
    this.uploaded = false;
    this.cdr.markForCheck();

    try {
      // Upload documents first (if selected)
      if (this.selectedDocumentFile) {
        await new Promise<void>((resolve, reject) => {
          this.uploadService
            .uploadDocument(this.claimId, this.selectedDocumentFile!)
            .subscribe({
              next: () => resolve(),
              error: (err) => reject(err),
            });
        });
      }

      // Upload damage image (if selected)
      if (this.selectedImageFile) {
        await new Promise<void>((resolve, reject) => {
          this.uploadService
            .uploadImage(this.claimId, this.selectedImageFile!)
            .subscribe({
              next: () => resolve(),
              error: (err) => reject(err),
            });
        });
      }

      this.uploaded = true;
      this.uploadComplete.emit();
    } catch (err) {
      console.error(err);
      this.snackBar.open('Upload failed. Please try again.', 'Close', { duration: 3000 });
    } finally {
      this.uploading = false;
      this.cdr.markForCheck();
    }
  }
}

