import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatButtonModule } from '@angular/material/button';

import { UploadService } from '../../../core/services/upload.service';

@Component({
  selector: 'app-image-upload',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
  ],
  templateUrl: './image-upload.html',
  styleUrl: './image-upload.css',
})
export class ImageUploadComponent {

  @Input()
  claimId!: number;

  private uploadService = inject(UploadService);

  selectedFile?: File;

  preview?: string;

  loading = false;

  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    if (!input.files?.length) {

      return;

    }

    this.selectedFile = input.files[0];

    const reader = new FileReader();

    reader.onload = () => {

      this.preview = reader.result as string;

    };

    reader.readAsDataURL(
      this.selectedFile
    );

  }

  upload(): void {

    if (!this.selectedFile) {

      return;

    }

    this.loading = true;

    this.uploadService.uploadImage(

      this.claimId,

      this.selectedFile,

    ).subscribe({

      next: () => {

        alert('Image uploaded successfully');

        this.loading = false;

      },

      error: (err) => {

        console.error(err);

        this.loading = false;

      }

    });

  }

}