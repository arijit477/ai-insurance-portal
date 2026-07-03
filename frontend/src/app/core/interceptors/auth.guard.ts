import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

import { TokenService } from '../services/token.service';

export const authGuard: CanActivateFn = () => {
  const tokenService = inject(TokenService);
  const router = inject(Router);

  const platformId = inject(PLATFORM_ID);
  const isBrowser = isPlatformBrowser(platformId);

  // During SSR we avoid redirect decisions based on localStorage.
  // The client will take over after hydration.
  if (!isBrowser) {
    return true;
  }

  if (tokenService.isLoggedIn()) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};

