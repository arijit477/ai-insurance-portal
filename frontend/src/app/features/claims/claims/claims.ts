import { Component, OnInit, ViewChild, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';

import { Claim } from '../../../core/models/claim/claim';
import { ClaimService } from '../../../core/services/claim.service';

import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatToolbarModule} from '@angular/material/toolbar';

@Component({
  selector: 'app-claims',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatProgressSpinnerModule,
    MatToolbarModule,
    MatCardModule,
  ],
  templateUrl: './claims.html',
  styleUrl: './claims.css',
})
export class ClaimsComponent implements OnInit {
  private claimService = inject(ClaimService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  displayedColumns = ['claim_number', 'title', 'claim_amount', 'status', 'submitted_at', 'actions'];

  dataSource = new MatTableDataSource<Claim>();

  loading = true;
  viewMode: 'table' | 'cards' = 'table';

  @ViewChild(MatPaginator)
  paginator!: MatPaginator;

  @ViewChild(MatSort)
  sort!: MatSort;

  ngOnInit(): void {
    this.loadClaims();
  }

  loadClaims(): void {
    this.claimService.getClaims().subscribe({
      next: (claims) => {
        this.dataSource.data = claims;
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
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

  applyFilter(event: Event): void {
    const filter = (event.target as HTMLInputElement).value;

    this.dataSource.filter = filter.trim().toLowerCase();
  }

  viewClaim(id: number): void {
    this.router.navigate(['/claims', id]);
  }

  getStatusClass(status: string): string {
    switch (status) {
      case 'Submitted':
        return 'submitted';

      case 'Under Review':
        return 'review';

      case 'AI Verified':
        return 'verified';

      case 'Approved':
        return 'approved';

      case 'Rejected':
        return 'rejected';

      case 'Paid':
        return 'paid';

      default:
        return '';
    }
  }

  editClaim(id: number): void {
    this.router.navigate(['/claims/edit', id]);
  }

  deleteClaim(id: number): void {
    if (!confirm('Delete this claim?')) {
      return;
    }

    this.claimService.deleteClaim(id).subscribe({
      next: () => {
        this.loadClaims();
      },

      error: (err) => {
        console.error(err);
      },
    });
  }
}
