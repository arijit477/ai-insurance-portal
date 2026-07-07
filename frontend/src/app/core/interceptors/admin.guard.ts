import { inject, PLATFORM_ID } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { TokenService } from '../services/token.service';
import { AuthService } from '../services/auth.service';
import { catchError, map, of } from 'rxjs';

export const adminGuard: CanActivateFn = () => {
  const tokenService = inject(TokenService);
  const authService = inject(AuthService);
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);
  const isBrowser = isPlatformBrowser(platformId);

  // During SSR we avoid redirect decisions based on localStorage.
  if (!isBrowser) {
    return true;
  }

  if (!tokenService.isLoggedIn()) {
    router.navigate(['/admin-login']);
    return false;
  }

  return authService.getProfile().pipe(
    map((user: any) => {
      if (user && user.role === 'Admin') {
        return true;
      }
      // If logged in but not admin, redirect to normal customer dashboard
      router.navigate(['/dashboard']);
      return false;
    }),
    catchError((err) => {
      console.error('Admin guard check failed:', err);
      authService.logout();
      router.navigate(['/admin-login']);
      return of(false);
    })
  );
};
