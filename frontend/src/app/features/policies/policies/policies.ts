import { Component, OnInit, ViewChild, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { MatTableDataSource } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';

import { Policy } from '../../../core/models/policy/policy';
import { PolicyService } from '../../../core/services/policy.service';

@Component({
  selector: 'app-policies',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatCardModule,
  ],
  templateUrl: './policies.html',
  styleUrl: './policies.css',
})
export class PoliciesComponent implements OnInit {

  private policyService = inject(PolicyService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  viewMode: 'table' | 'cards' = 'table';

  displayedColumns = [
    'policy_number',
    'premium_paid',
    'start_date',
    'end_date',
    'status',
    'actions',
  ];

  dataSource = new MatTableDataSource<Policy>();

  @ViewChild(MatPaginator)
  paginator!: MatPaginator;

  @ViewChild(MatSort)
  sort!: MatSort;

  ngOnInit(): void {
    this.loadPolicies();
  }

  loadPolicies(): void {
    this.policyService.getPolicies().subscribe({
      next: (response) => {
        this.dataSource.data = response;
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
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

  viewPolicy(id: number): void {
    this.router.navigate([
      '/policies',
      id,
    ]);
  }

  getStatusClass(status: string): string {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'active';
      case 'inactive':
        return 'inactive';
      case 'pending':
        return 'pending';
      case 'lapsed':
        return 'lapsed';
      default:
        return '';
    }
  }

}