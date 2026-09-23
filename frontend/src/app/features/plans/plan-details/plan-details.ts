import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDividerModule } from '@angular/material/divider';

import { InsurancePlan } from '../../../core/models/insurance/insurance-plan';
import { PlanService } from '../../../core/services/plan.service';
import { PolicyService } from '../../../core/services/policy.service';
import { AuthService } from '../../../core/services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-plan-details',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatDividerModule,
  ],
  templateUrl: './plan-details.html',
  styleUrl: './plan-details.css',
})
export class PlanDetailsComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private planService = inject(PlanService);
  private policyService = inject(PolicyService);
  private authService = inject(AuthService);
  private snackBar = inject(MatSnackBar);
  private cdr = inject(ChangeDetectorRef);

  loading = true;
  purchasing = false;
  plan!: InsurancePlan;

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadPlan(id);
  }

  loadPlan(id: number): void {
    this.planService.getPlan(id).subscribe({
      next: (response) => {
        this.plan = response;
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

  private loadRazorpayScript(): Promise<boolean> {
    return new Promise((resolve) => {
      if (typeof window === 'undefined') {
        resolve(false);
        return;
      }
      if ((window as any).Razorpay) {
        resolve(true);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  }

  purchasePolicy(): void {
    this.purchasing = true;
    this.cdr.markForCheck();

    this.loadRazorpayScript().then((loaded) => {
      if (!loaded) {
        this.snackBar.open('Failed to load payment gateway. Please check your network.', 'Close', { duration: 4000 });
        this.purchasing = false;
        this.cdr.markForCheck();
        return;
      }

      this.policyService.createPolicy({ plan_id: this.plan.id }).subscribe({
        next: (orderInfo) => {
          this.authService.getProfile().subscribe({
            next: (user) => {
              this.openRazorpayModal(orderInfo, user);
            },
            error: () => {
              this.openRazorpayModal(orderInfo, null);
            }
          });
        },
        error: (err) => {
          console.error(err);
          this.snackBar.open(err.error?.detail || 'Failed to initiate purchase.', 'Close', { duration: 4000 });
          this.purchasing = false;
          this.cdr.markForCheck();
        },
      });
    });
  }

  private openRazorpayModal(orderInfo: any, user: any): void {
    const isMock = !orderInfo.key_id ||
      orderInfo.key_id === 'rzp_test_placeholder_key' ||
      (orderInfo.order_id && orderInfo.order_id.startsWith('order_mock_'));

    if (isMock) {
      const mockPayId = 'pay_mock_' + Math.random().toString(36).substring(2, 10).toUpperCase();
      const mockSig = 'sig_mock_' + Math.random().toString(36).substring(2, 10).toUpperCase();
      this.policyService.verifyPayment({
        razorpay_order_id: orderInfo.order_id,
        razorpay_payment_id: mockPayId,
        razorpay_signature: mockSig,
      }).subscribe({
        next: () => {
          this.snackBar.open('Payment successful! Your policy is now active.', 'Close', { duration: 4000 });
          this.router.navigate(['/policies']);
        },
        error: (err) => {
          console.error('Verification failed:', err);
          this.snackBar.open(err.error?.detail || 'Payment verification failed.', 'Close', { duration: 5000 });
          this.purchasing = false;
          this.cdr.markForCheck();
        }
      });
      return;
    }

    const options = {
      key: orderInfo.key_id,
      amount: orderInfo.amount,
      currency: orderInfo.currency,
      name: 'AI Insurance Portal',
      description: `Purchase of ${this.plan.plan_name}`,
      order_id: orderInfo.order_id,
      handler: (response: any) => {
        this.policyService.verifyPayment({
          razorpay_order_id: response.razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_signature: response.razorpay_signature,
        }).subscribe({
          next: () => {
            this.snackBar.open('Payment successful! Your policy is now active.', 'Close', { duration: 4000 });
            this.router.navigate(['/policies']);
          },
          error: (err) => {
            console.error('Verification failed:', err);
            this.snackBar.open(err.error?.detail || 'Payment verification failed. Please contact support.', 'Close', { duration: 5000 });
            this.purchasing = false;
            this.cdr.markForCheck();
          }
        });
      },
      prefill: {
        name: user?.full_name || '',
        email: user?.email || '',
      },
      theme: {
        color: '#3f51b5',
      },
      modal: {
        ondismiss: () => {
          this.purchasing = false;
          this.cdr.markForCheck();
        }
      }
    };

    try {
      const rzp = new (window as any).Razorpay(options);
      rzp.on('payment.failed', (response: any) => {
        console.error('Payment failed:', response.error);
        this.snackBar.open(`Payment failed: ${response.error.description}`, 'Close', { duration: 5000 });
        this.purchasing = false;
        this.cdr.markForCheck();
      });
      rzp.open();
    } catch (e: any) {
      console.error('Error opening Razorpay:', e);
      this.snackBar.open('Could not open payment gateway. Please check browser popups or try again.', 'Close', { duration: 5000 });
      this.purchasing = false;
      this.cdr.markForCheck();
    }
  }
}
