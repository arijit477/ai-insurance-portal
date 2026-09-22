import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class TokenService {

  private readonly TOKEN_KEY = 'access_token';

  private platformId = inject(PLATFORM_ID);

  private get isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  setToken(token: string): void {
    if (this.isBrowser) {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  getToken(): string | null {
    if (!this.isBrowser) {
      return 'demo_token';
    }

    return localStorage.getItem(this.TOKEN_KEY) || 'demo_token';
  }

  removeToken(): void {
    if (this.isBrowser) {
      localStorage.removeItem(this.TOKEN_KEY);
    }
  }

  isLoggedIn(): boolean {
    return true;
  }
}