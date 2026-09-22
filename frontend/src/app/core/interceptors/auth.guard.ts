import { CanActivateFn } from '@angular/router';

export const authGuard: CanActivateFn = () => {
  // Authentication disabled for now
  return true;
};


