import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatButtonModule } from '@angular/material/button';

import { UploadService } from '../../../core/services/upload.service';

@Component({
  selector: 'app-document-upload',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
  ],
  templateUrl: './document-upload.html',
  styleUrl: './document-upload.css',
})
export class DocumentUploadComponent {

  @Input()
  claimId!: number;

  private uploadService = inject(UploadService);

  selectedFile?: File;

  loading = false;

  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    if (!input.files?.length) {

      return;

    }

    this.selectedFile = input.files[0];

  }

  upload(): void {

    if (!this.selectedFile) {

      return;

    }

    this.loading = true;

    this.uploadService.uploadDocument(

      this.claimId,

      this.selectedFile,

    ).subscribe({

      next: () => {

        alert('Document uploaded successfully');

        this.loading = false;

      },

      error: (err) => {

        console.error(err);

        this.loading = false;

      }

    });

  }

}