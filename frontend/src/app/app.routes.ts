import { Routes } from '@angular/router';

import { LoginComponent } from './features/auth/login/login';
import { RegisterComponent } from './features/auth/register/register';
import { AdminLoginComponent } from './features/auth/admin-login/admin-login';

import { DashboardComponent } from './features/dashboard/dashboard';
import { PlansComponent } from './features/plans/plans/plans';
import { PoliciesComponent } from './features/policies/policies/policies';
import { PolicyDetailsComponent } from './features/policies/policies-details/policies-details';
import { ClaimsComponent } from './features/claims/claims/claims';
import { AiReport } from './features/ai-report/ai-report';
import { AiReportsList } from './features/ai-report/ai-reports-list/ai-reports-list';
import { Admin } from './features/admin/admin';
import { ProfileComponent } from './features/profile/profile';
import { NotFound } from './shared/not-found/not-found';
import { authGuard } from './core/interceptors/auth.guard';
import { adminGuard } from './core/interceptors/admin.guard';
import { CreateClaimComponent } from './features/claims/create-claim/create-claim';
import { PlanDetailsComponent } from './features/plans/plan-details/plan-details';
import { ClaimDetails } from './features/claims/claim-details/claim-details';
import { UploadPageComponent } from './features/upload/upload-page/upload-page';
import { Layout } from './shared/layout/layout';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full',
  },

  {
    path: 'login',
    component: LoginComponent,
  },

  {
    path: 'register',
    component: RegisterComponent,
  },

  {
    path: 'admin-login',
    component: AdminLoginComponent,
  },

  {
    path: '',
    component: Layout,
    canActivate: [authGuard],
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent,
      },
      {
        path: 'plans',
        component: PlansComponent,
      },
      {
        path: 'plans/:id',
        component: PlanDetailsComponent,
      },
      {
        path: 'policies',
        component: PoliciesComponent,
      },
      {
        path: 'policies/:id',
        component: PolicyDetailsComponent,
      },
      {
        path: 'claims/create',
        component: CreateClaimComponent,
      },
      {
        path: 'claims/:id',
        component: ClaimDetails,
      },
      {
        path: 'claims',
        component: ClaimsComponent,
      },
      {
        path: 'upload/:claimId',
        component: UploadPageComponent,
      },
      {
        path: 'ai-reports',
        component: AiReportsList,
      },
      {
        path: 'ai-report/:claimId',
        component: AiReport,
      },
      {
        path: 'admin',
        component: Admin,
        canActivate: [adminGuard],
      },
      {
        path: 'profile',
        component: ProfileComponent,
      },
    ]
  },

  {
    path: '**',
    component: NotFound,
  },
];

