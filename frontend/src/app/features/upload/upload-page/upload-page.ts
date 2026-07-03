import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { ClaimBundleUploadComponent } from '../claim-bundle-upload/claim-bundle-upload';

@Component({
  selector: 'app-upload-page',
  standalone: true,
  imports: [
    CommonModule,
    ClaimBundleUploadComponent,
  ],
  template: `
    <app-claim-bundle-upload [claimId]="claimId"></app-claim-bundle-upload>
  `,
})
export class UploadPageComponent {
  private route = inject(ActivatedRoute);

  claimId: number = Number(this.route.snapshot.paramMap.get('claimId'));
}
