import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject, Injector, PLATFORM_ID, runInInjectionContext } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

import { TokenService } from '../services/token.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {

  const tokenService = inject(TokenService);
  const injector = inject(Injector);
  const platformId = inject(PLATFORM_ID);
  const isBrowser = isPlatformBrowser(platformId);

  const token = tokenService.getToken();

  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && isBrowser) {
        tokenService.removeToken();
        // Lazy inject Router via runInInjectionContext to avoid SSR circular dependency
        runInInjectionContext(injector, () => {
          inject(Router).navigate(['/login']);
        });
      }
      return throwError(() => error);
    })
  );

};