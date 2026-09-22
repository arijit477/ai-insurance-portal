import { CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = () => {
  // Authentication disabled for now
  return true;
};

