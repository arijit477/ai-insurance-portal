import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

import { ClaimService } from '../../../core/services/claim.service';
import { CreateClaim } from '../../../core/models/claim/create-claim';
import { PolicyService } from '../../../core/services/policy.service';
import { Policy } from '../../../core/models/policy/policy';
import { PlanService } from '../../../core/services/plan.service';
import { InsurancePlan } from '../../../core/models/insurance/insurance-plan';

interface PolicyWithPlan {
  id: number;
  policy_number: string;
  plan_name: string;
  category: string;
}

@Component({
  selector: 'app-create-claim',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
  ],
  templateUrl: './create-claim.html',
  styleUrl: './create-claim.css',
})
export class CreateClaimComponent implements OnInit {
  private fb = inject(FormBuilder);
  private claimService = inject(ClaimService);
  private router = inject(Router);
  private policyService = inject(PolicyService);
  private planService = inject(PlanService);
  private cdr = inject(ChangeDetectorRef);

  loading = false;
  loadingPolicies = true;
  policies: Policy[] = [];
  plans: InsurancePlan[] = [];
  policiesWithPlans: PolicyWithPlan[] = [];

  ngOnInit(): void {
    forkJoin({
      policies: this.policyService.getPolicies(),
      plans: this.planService.getPlans()
    }).subscribe({
      next: (result) => {
        this.policies = result.policies;
        this.plans = result.plans;

        const planMap = new Map(this.plans.map(p => [p.id, p]));
        this.policiesWithPlans = this.policies.map(pol => {
          const plan = planMap.get(pol.plan_id);
          return {
            id: pol.id,
            policy_number: pol.policy_number,
            plan_name: plan ? plan.plan_name : 'Unknown Plan',
            category: plan ? plan.category : 'Unknown'
          };
        });

        this.loadingPolicies = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load policies or plans:', err);
        this.loadingPolicies = false;
        this.cdr.markForCheck();
      },
    });
  }

  claimForm = this.fb.group({
    policy_id: [null as number | null, Validators.required],
    title: ['', [Validators.required, Validators.minLength(5), Validators.maxLength(150)]],
    description: ['', [Validators.required, Validators.minLength(10)]],
    claim_amount: [null as number | null, [Validators.required, Validators.min(1)]],
  });

  submit(): void {
    if (this.claimForm.invalid) {
      return;
    }

    this.loading = true;
    this.cdr.markForCheck();

    const rawForm = this.claimForm.getRawValue();
    const selectedPolicy = this.policiesWithPlans.find(p => p.id === rawForm.policy_id);

    const request: CreateClaim = {
      policy_id: rawForm.policy_id!,
      title: rawForm.title!,
      description: rawForm.description!,
      claim_amount: rawForm.claim_amount!,
      claim_type: selectedPolicy ? `${selectedPolicy.category} Claim` : 'Other Claim'
    };

    this.claimService.createClaim(request).subscribe({
      next: (claim) => {
        this.router.navigate(['/claims', claim.id]);
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }
}

